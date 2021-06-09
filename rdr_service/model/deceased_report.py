from sqlalchemy import Column, Date, ForeignKey, event, Integer, String
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from rdr_service.model.base import Base, model_insert_listener, model_update_listener
from rdr_service.model.utils import Enum, UTCDateTime, UTCDateTime6
from rdr_service.participant_enums import DeceasedNotification, DeceasedReportDenialReason, DeceasedReportStatus


class DeceasedReportBase:
    created = Column("created", UTCDateTime, nullable=False)
    modified = Column("modified", UTCDateTime, nullable=False)

    @declared_attr
    def participantId(self):
        return Column("participant_id", Integer, ForeignKey("participant.participant_id"), nullable=False)
    dateOfDeath = Column("date_of_death", Date)
    causeOfDeath = Column("cause_of_death", String(1024))
    notification = Column("notification", Enum(DeceasedNotification), nullable=False)
    notificationOther = Column("notification_other", String(1024))
    reporterName = Column('reporter_name', String(255))
    reporterRelationship = Column('reporter_relationship', String(8))
    reporterEmail = Column('reporter_email', String(255))
    reporterPhone = Column('reporter_phone', String(16))

    @declared_attr
    def authorId(self):
        return Column("author_id", Integer, ForeignKey("api_user.id"), nullable=False)
    authored = Column("authored", UTCDateTime, nullable=False)

    @declared_attr
    def reviewerId(self):
        return Column("reviewer_id", Integer, ForeignKey("api_user.id"))
    reviewed = Column("reviewed", UTCDateTime)
    status = Column("status", Enum(DeceasedReportStatus), nullable=False)
    denialReason = Column("denial_reason", Enum(DeceasedReportDenialReason))
    denialReasonOther = Column("denial_reason_other", String(1024))

    @declared_attr
    def author(self):
        return relationship("ApiUser", foreign_keys=self.authorId, lazy='joined')

    @declared_attr
    def reviewer(self):
        return relationship("ApiUser", foreign_keys=self.reviewerId, lazy='joined')

    @declared_attr
    def participant(self):
        return relationship("Participant", foreign_keys=self.participantId)


class HistoryTableMixin:
    revisionAction = Column('revision_action', String(8), default='insert')
    revisionId = Column(
        "revision_id", Integer, primary_key=True, autoincrement=True, nullable=False, index=True
    )
    revisionTimestamp = Column("revision_timestamp", UTCDateTime6, default='CURRENT_TIMESTAMP(6)')


class DeceasedReport(DeceasedReportBase, Base):
    __tablename__ = 'deceased_report'
    id = Column("id", Integer, primary_key=True, autoincrement=True, nullable=False)


class ReportHistory(DeceasedReportBase, HistoryTableMixin, Base):
    __tablename__ = 'deceased_report_history'
    id = Column("id", Integer, nullable=False, primary_key=True, autoincrement=False)


event.listen(DeceasedReport, "before_insert", model_insert_listener)
event.listen(DeceasedReport, "before_update", model_update_listener)
