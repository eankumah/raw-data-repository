"""block_fieds_genomic_set_member

Revision ID: 968bbe502102
Revises: 47199ca259e2
Create Date: 2021-11-19 12:59:58.399301

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
revision = '968bbe502102'
down_revision = '47199ca259e2'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()


def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('genomic_set_member', sa.Column('block_research', sa.SmallInteger(), nullable=False))
    op.add_column('genomic_set_member', sa.Column('block_research_reason', sa.String(length=255), nullable=True))
    op.add_column('genomic_set_member', sa.Column('block_results', sa.SmallInteger(), nullable=False))
    op.add_column('genomic_set_member', sa.Column('block_results_reason', sa.String(length=255), nullable=True))
    op.add_column('genomic_set_member', sa.Column('ignore_flag', sa.SmallInteger(), nullable=False))
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('genomic_set_member', 'ignore_flag')
    op.drop_column('genomic_set_member', 'block_results_reason')
    op.drop_column('genomic_set_member', 'block_results')
    op.drop_column('genomic_set_member', 'block_research_reason')
    op.drop_column('genomic_set_member', 'block_research')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

