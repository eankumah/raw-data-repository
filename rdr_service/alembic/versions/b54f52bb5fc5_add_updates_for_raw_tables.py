"""add_updates_for_raw_tables

Revision ID: b54f52bb5fc5
Revises: 4b259a4a4397
Create Date: 2021-09-09 10:00:21.921079

"""
from alembic import op
import sqlalchemy as sa
import rdr_service.model.utils


from rdr_service.participant_enums import PhysicalMeasurementsStatus, QuestionnaireStatus, OrderStatus
from rdr_service.participant_enums import WithdrawalStatus, WithdrawalReason, SuspensionStatus, QuestionnaireDefinitionStatus
from rdr_service.participant_enums import EnrollmentStatus, Race, SampleStatus, OrganizationType, BiobankOrderStatus
from rdr_service.participant_enums import OrderShipmentTrackingStatus, OrderShipmentStatus
from rdr_service.participant_enums import MetricSetType, MetricsKey, GenderIdentity
from rdr_service.model.base import add_table_history_table, drop_table_history_table
from rdr_service.model.code import CodeType
from rdr_service.model.site_enums import SiteStatus, EnrollingStatus, DigitalSchedulingStatus, ObsoleteStatus

# revision identifiers, used by Alembic.
revision = 'b54f52bb5fc5'
down_revision = '4b259a4a4397'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()


def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        """Update genomic_aw1_raw aw1r
        Set aw1r.genome_type = aw1r.test_name
        Where aw1r.genome_type is null"""
    )

    op.execute(
        """Update genomic_aw2_raw aw2r
        Inner Join genomic_set_member gsm
        On aw2r.sample_id = gsm.sample_id
        Set aw2r.genome_type = gsm.genome_type
        Where aw2r.genome_type is null"""
    )
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

