import logging

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UnicodeText, event
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from rdr_service.model.field_types import BlobUTF8
from rdr_service.model.base import Base, model_insert_listener, model_update_listener
from rdr_service.model.biobank_mail_kit_order import BiobankMailKitOrder
from rdr_service.model.utils import Enum, UTCDateTime, UTCDateTime6
from rdr_service.participant_enums import BiobankOrderStatus


class BiobankOrderBase(object):
    """An order requesting samples.

  The order contains a list of samples stored in BiobankOrderedSample; the actual delivered and
  stored samples are tracked in BiobankStoredSample. Our reconciliation report compares the two.
  """

    _MAIN_ID_SYSTEM = "https://orders.mayomedicallaboratories.com"

    biobankOrderId = Column("biobank_order_id", String(80), primary_key=True)
    """
    The globally unique ID created by HealthPro when a biobank order is created. This order ID is pushed
    to MayoLINK when the biobank order is created in their system. As requested/suggested by Mayo,
    it should be 12 alphanumeric characters long.
    """

    version = Column("version", Integer, nullable=False)
    """
    Incrementing version, starts at 1 and is incremented on each update. The history table will have multiple versions
    ranging from 1 to the number of times the record has been updated. Each of these different versions will show
    the values that have changed.
    """

    sourceUsername = Column("source_username", String(255))
    """The user that created the order"""

    collectedUsername = Column("collected_username", String(255))
    """The username of the user who collected the order"""

    processedUsername = Column("processed_username", String(255))
    """The username of the user who processed the order"""

    finalizedUsername = Column("finalized_username", String(255))
    """The username of the user who finalized the order"""
    finalizedTime = Column('finalized_time', UTCDateTime)
    """Backfilled using a finalized time from the related `biobank_ordered_sample` records"""

    # cancelled finalized order may still be shipped to biobank for destruction
    # orderstatus can be cancelled/amended/restored
    # A null value or UNSET == finalized (i.e. the current accepted value)

    orderStatus = Column("order_status", Enum(BiobankOrderStatus))
    """The status of the biobank order"""
    amendedReason = Column("amended_reason", UnicodeText)
    """
    The clinic's reason for why the order was amended. A cancelled or edited order must have a reason.
    Set on the old row because cancelled orders don't create a new row like amended orders do.
    """
    lastModified = Column("last_modified", UTCDateTime)
    """The datetime of the last update to the order"""

    restoredUsername = Column("restored_username", String(255))
    """The username of the user who uncancelled the order"""
    restoredTime = Column("restored_time", UTCDateTime)
    """The datetime an order was uncancelled"""

    amendedUsername = Column("amended_username", String(255))
    """The username of the user who amended the order"""
    amendedTime = Column("amended_time", UTCDateTime)
    """The time at which the biobank order was amended"""

    cancelledUsername = Column("cancelled_username", String(255))
    """The username of the user who cancelled the order"""
    cancelledTime = Column("cancelled_time", UTCDateTime)
    """The datetime at which the biobank order was cancelled"""

    created = Column("created", UTCDateTime, nullable=False)
    """The time at which a HealthPro user creates a biobank order; autogenerated by HealthPro"""
    collectedNote = Column("collected_note", UnicodeText)
    """
    Text input by the user to capture additional notes relevant to the sample collection process
    (ex. “incomplete draw for EDTA sample number 1. Only 2 of the required 4 mL were drawn”)
    """
    processedNote = Column("processed_note", UnicodeText)
    """
    Text inputted by the user to capture additional notes relevant to the sample processing process
    (ex. “Centrifuge was not cooled to the proper temperature for blood spin down.
    All samples were spun at RT instead of 4C”)
    """
    finalizedNote = Column("finalized_note", UnicodeText)
    """
    Text inputted by the user to capture additional notes relevant to the sample finalization process
    (ex. “Samples are prepared for shipment and stored in the 4C fridge in Room 520A”)
    """

    orderOrigin = Column("order_origin", String(80))
    """
    Where it came from - HealthPro, etc.
    @rdr_dictionary_show_unique_values
    """

    @declared_attr
    def participantId(cls):
        """
        PMI-specific ID generated by the RDR and used for tracking/linking participant data.
        10-character string beginning with P.
        """
        return Column("participant_id", Integer, ForeignKey("participant.participant_id"), nullable=False)

    @declared_attr
    def amendedBiobankOrderId(cls):
        """If a biobank order is amended, it gets its own unique id"""
        return Column("amended_biobank_order_id", String(80), ForeignKey("biobank_order.biobank_order_id"))

    # For syncing new orders.
    @declared_attr
    def logPositionId(cls):
        """@rdr_dictionary_internal_column"""
        return Column("log_position_id", Integer, ForeignKey("log_position.log_position_id"), nullable=False)

    # The site that created the order -- createdInfo['site'] in the resulting JSON
    @declared_attr
    def sourceSiteId(cls):
        """The site that created the order"""
        return Column("source_site_id", Integer, ForeignKey("site.site_id"))

    # The site that collected the order -- collectedInfo['site'] in the resulting JSON
    @declared_attr
    def collectedSiteId(cls):
        """
        The site at which the order was collected
        (usually same site between collected, amended, cancelled, but not always)
        """
        return Column("collected_site_id", Integer, ForeignKey("site.site_id"))

    # The site that processed the order -- processedInfo['site'] in the resulting JSON
    @declared_attr
    def processedSiteId(cls):
        """The site id for the site that processed the order"""
        return Column("processed_site_id", Integer, ForeignKey("site.site_id"))

    # The site that finalized the order -- finalizedInfo['site'] in the resulting JSON
    @declared_attr
    def finalizedSiteId(cls):
        """The id of the site that finalized the order"""
        return Column("finalized_site_id", Integer, ForeignKey("site.site_id"))

    @declared_attr
    def restoredSiteId(cls):
        """If an order was uncancelled"""
        return Column("restored_site_id", Integer, ForeignKey("site.site_id"))

    @declared_attr
    def amendedSiteId(cls):
        """The site that amended the order"""
        return Column("amended_site_id", Integer, ForeignKey("site.site_id"))

    @declared_attr
    def cancelledSiteId(cls):
        """The site that cancelled the order"""
        return Column("cancelled_site_id", Integer, ForeignKey("site.site_id"))


class BiobankOrder(BiobankOrderBase, Base):
    __tablename__ = "biobank_order"
    logPosition = relationship("LogPosition")
    identifiers = relationship("BiobankOrderIdentifier", cascade="all, delete-orphan")
    samples = relationship("BiobankOrderedSample", cascade="all, delete-orphan")
    mailKitOrders = relationship(BiobankMailKitOrder, cascade="all, delete-orphan")
    questSiteAddress = relationship("BiobankQuestOrderSiteAddress", uselist=False, cascade="all, delete-orphan",
                                    backref="biobank_order")


class BiobankQuestOrderSiteAddress(Base):
    __tablename__ = "biobank_quest_order_site_address"
    id = Column("id", Integer, primary_key=True, autoincrement=True, nullable=False)
    address1 = Column("address1", String(500))
    address2 = Column("address2", String(500))
    city = Column("city", String(80))
    state = Column("state", String(50))
    zipCode = Column("zip_code", String(50))

    @declared_attr
    def biobankOrderId(cls):
        return Column("biobank_order_id", String(80), ForeignKey("biobank_order.biobank_order_id"), nullable=False)


class BiobankOrderIdentifierBase(object):
    system = Column("system", String(80), primary_key=True)
    """
    Whether the order originated from Mayo Clinic or HealthPro
    @rdr_dictionary_show_unique_values
    """
    value = Column("value", String(80), primary_key=True, index=True)
    """The internal ID of the system"""

    @declared_attr
    def biobankOrderId(cls):
        return Column("biobank_order_id", String(80), ForeignKey("biobank_order.biobank_order_id"),
                      primary_key=True, nullable=False)

    def __str__(self):
        return f'{self.value} (system: {self.system})'


class BiobankOrderIdentifier(BiobankOrderIdentifierBase, Base):
    """Arbitrary IDs for a BiobankOrder in other systems.

  Other clients may create these, but they must be unique within each system.
  """

    __tablename__ = "biobank_order_identifier"


class BiobankOrderedSampleBase(object):
    @declared_attr
    def biobankOrderId(cls):
        """
        The globally unique ID created by HealthPro when a biobank order is created.
        This order ID is pushed to MayoLINK when the biobank order is created in their system.
        As requested/suggested by Mayo, it should be 12 alphanumeric characters long.
        """
        return Column("order_id", String(80), ForeignKey("biobank_order.biobank_order_id"), primary_key=True)

    test = Column("test", String(80), primary_key=True)
    """
    What the test ordered is.
    Unique within an order, though the same test may be redone in another order for the participant.
    @rdr_dictionary_show_unique_values
    """

    description = Column("description", UnicodeText, nullable=False)
    """Free text description of the sample"""
    processingRequired = Column("processing_required", Boolean, nullable=False)
    """HealthPro biobank order if clinic marks it as 'requires processing'"""
    collected = Column("collected", UTCDateTime)
    """The time at which biobank sample collection is completed. Input by user"""
    processed = Column("processed", UTCDateTime)
    """The time at which this tube’s processing (i.e. centrifugation) is completed. Input by user."""
    finalized = Column("finalized", UTCDateTime)
    """The time at which this tube’s processing (i.e., centrifugation) is completed. Input by user."""


class BiobankOrderedSample(BiobankOrderedSampleBase, Base):
    """Samples listed by a Biobank order.

  These are distinct from BiobankStoredSamples, which tracks received samples. The two should
  eventually match up, but we see BiobankOrderedSamples first and track them separately.
  """

    __tablename__ = "biobank_ordered_sample"


class BiobankOrderHistory(BiobankOrderBase, Base):
    __tablename__ = "biobank_history"

    version = Column("version", Integer, primary_key=True)
    """
    Incrementing version, starts at 1 and is incremented on each update. The history table will have multiple versions
    ranging from 1 to the number of times the record has been updated. Each of these different versions will show
    the values that have changed.
    """


class BiobankOrderedSampleHistory(BiobankOrderedSampleBase, Base):
    __tablename__ = "biobank_ordered_sample_history"

    version = Column("version", Integer, primary_key=True)
    """
    Incrementing version, starts at 1 and is incremented on each update. The history table will have multiple versions
    ranging from 1 to the number of times the record has been updated. Each of these different versions will show
    the values that have changed.
    """


class BiobankOrderIdentifierHistory(BiobankOrderIdentifierBase, Base):
    __tablename__ = "biobank_order_identifier_history"

    version = Column("version", Integer, primary_key=True)
    """
    Incrementing version, starts at 1 and is incremented on each update. The history table will have multiple versions
    ranging from 1 to the number of times the record has been updated. Each of these different versions will show
    the values that have changed.
    """


class MayolinkCreateOrderHistory(Base):
    __tablename__ = "mayolink_create_order_history"

    id = Column("id", Integer, primary_key=True, autoincrement=True, nullable=False)
    """Id of the biobank order"""
    created = Column("created", UTCDateTime6, nullable=True)
    """When the order was created"""
    # have mysql always update the modified data when the record is changed
    modified = Column("modified", UTCDateTime6, nullable=True)
    requestParticipantId = Column("request_participant_id", Integer)
    """Participant_id tied to that request"""
    requestTestCode = Column("request_test_code", String(500))
    """Test code for the test performed on that biobank sample"""
    requestOrderId = Column("response_order_id", String(80))
    """Order id for the request"""
    requestOrderStatus = Column("response_order_status", String(80))
    """Status of order in request"""
    requestPayload = Column("request_payload", BlobUTF8)
    """Payload tied to that request"""
    responsePayload = Column("response_payload", BlobUTF8)
    """Payload tied to response to a request"""


class BiobankSpecimenBase(object):
    id = Column("id", Integer, primary_key=True, autoincrement=True, nullable=False)
    created = Column("created", UTCDateTime6, nullable=True)
    modified = Column("modified", UTCDateTime6, nullable=True)


class SpecimenAliquotBase(object):
    sampleType = Column("sample_type", String(80))
    status = Column("status", String(100))
    disposalReason = Column("disposal_reason", String(80))
    disposalDate = Column("disposal_date", UTCDateTime)
    freezeThawCount = Column("freeze_thaw_count", Integer)
    location = Column("location", String(200))
    quantity = Column("quantity", String(80))
    quantityUnits = Column("quantity_units", String(80))
    processingCompleteDate = Column("processing_complete_date", UTCDateTime)
    deviations = Column('deviations', JSON)


class BiobankSpecimen(Base, BiobankSpecimenBase, SpecimenAliquotBase):
    __tablename__ = "biobank_specimen"

    aliquots = relationship("BiobankAliquot", cascade="all",
                              foreign_keys="BiobankAliquot.specimen_id",
                              order_by="BiobankAliquot.rlimsId")
    attributes = relationship("BiobankSpecimenAttribute", cascade="all",
                              foreign_keys="BiobankSpecimenAttribute.specimen_id",
                              order_by="BiobankSpecimenAttribute.name")
    rlimsId = Column("rlims_id", String(80), unique=True)
    biobankId = Column("biobank_id", Integer, ForeignKey("participant.biobank_id"), nullable=False)
    orderId = Column("order_id", String(80), nullable=False)
    testCode = Column("test_code", String(80))
    repositoryId = Column("repository_id", String(80))
    studyId = Column("study_id", String(80))
    cohortId = Column("cohort_id", String(80))
    collectionDate = Column("collection_date", UTCDateTime)
    confirmedDate = Column("confirmed_date", UTCDateTime)


class BiobbankSpecimenAliquotBase(object):
    @declared_attr
    def specimen_id(cls):
        return Column("specimen_id", Integer, ForeignKey("biobank_specimen.id"))
    @declared_attr
    def specimen_rlims_id(cls):
        return Column("specimen_rlims_id", String(80), ForeignKey("biobank_specimen.rlims_id"))


class BiobankSpecimenAttribute(Base, BiobankSpecimenBase, BiobbankSpecimenAliquotBase):
    __tablename__ = "biobank_specimen_attribute"
    name = Column("name", String(80))
    value = Column("value", String(80))


class BiobankAliquot(Base, BiobankSpecimenBase, BiobbankSpecimenAliquotBase, SpecimenAliquotBase):
    __tablename__ = "biobank_aliquot"
    @declared_attr
    def specimen_id(cls):
        return Column("specimen_id", Integer, ForeignKey("biobank_specimen.id"))

    @declared_attr
    def parent_aliquot_id(cls):
        return Column("parent_aliquot_id", Integer, ForeignKey('biobank_aliquot.id'))
    @declared_attr
    def parent_aliquot_rlims_id(cls):
        return Column("parent_aliquot_rlims_id", String(80))
    rlimsId = Column("rlims_id", String(80), unique=True)
    childPlanService = Column("child_plan_service", String(100))
    initialTreatment = Column("initial_treatment", String(100))
    containerTypeId = Column("container_type_id", String(100))

    datasets = relationship("BiobankAliquotDataset", cascade="all",
                            foreign_keys="BiobankAliquotDataset.aliquot_id",
                            order_by="BiobankAliquotDataset.rlimsId")
    aliquots = relationship("BiobankAliquot", cascade="all",
                            foreign_keys="BiobankAliquot.parent_aliquot_id",
                            order_by="BiobankAliquot.rlimsId")


class BiobankAliquotDataset(Base, BiobankSpecimenBase):
    __tablename__ = "biobank_aliquot_dataset"
    @declared_attr
    def aliquot_id(cls):
        return Column("aliquot_id", Integer, ForeignKey("biobank_aliquot.id"))
    @declared_attr
    def aliquot_rlims_id(cls):
        return Column("aliquot_rlims_id", String(80), ForeignKey("biobank_aliquot.rlims_id"))
    rlimsId = Column("rlims_id", String(80), unique=True)
    name = Column("name", String(80))
    status = Column("status", String(80))

    datasetItems = relationship("BiobankAliquotDatasetItem", cascade="all, delete-orphan",
                                foreign_keys="BiobankAliquotDatasetItem.dataset_id",
                                order_by="BiobankAliquotDatasetItem.paramId")


class BiobankAliquotDatasetItem(Base, BiobankSpecimenBase):
    __tablename__ = "biobank_aliquot_dataset_item"
    @declared_attr
    def dataset_id(cls):
        return Column("dataset_id", Integer, ForeignKey("biobank_aliquot_dataset.id"))
    @declared_attr
    def dataset_rlims_id(cls):
        return Column("dataset_rlims_id", String(80), ForeignKey("biobank_aliquot_dataset.rlims_id"))
    paramId = Column("param_id", String(80))
    displayValue = Column("display_value", String(80))
    displayUnits = Column("display_units", String(80))


def before_item_delete(_, __, dataset_item: BiobankAliquotDatasetItem):
    logging.info(
        f'deleting dataset item with id "{dataset_item.id}", paramId "{dataset_item.paramId}" '
        f'and dataset rlims id "{dataset_item.dataset_rlims_id}"'
    )


event.listen(BiobankAliquotDatasetItem, 'before_delete', before_item_delete)


for model_class in [MayolinkCreateOrderHistory, BiobankSpecimen, BiobankSpecimenAttribute,
                    BiobankAliquot, BiobankAliquotDataset, BiobankAliquotDatasetItem]:
    event.listen(model_class, "before_insert", model_insert_listener)
    event.listen(model_class, "before_update", model_update_listener)
