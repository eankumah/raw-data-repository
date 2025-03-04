"""w1il job id tracking

Revision ID: 33b34f5ae271
Revises: f69e4a978a1f, 78ab5fe99ad1
Create Date: 2022-03-22 09:50:03.100166

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
revision = '33b34f5ae271'
down_revision = ('f69e4a978a1f', '78ab5fe99ad1')
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()



def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('genomic_set_member', sa.Column('cvl_w1il_hdr_job_run_id', sa.Integer(), nullable=True))
    op.add_column('genomic_set_member', sa.Column('cvl_w1il_pgx_job_run_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'genomic_set_member', 'genomic_job_run', ['cvl_w1il_pgx_job_run_id'], ['id'])
    op.create_foreign_key(None, 'genomic_set_member', 'genomic_job_run', ['cvl_w1il_hdr_job_run_id'], ['id'])
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'genomic_set_member', type_='foreignkey')
    op.drop_constraint(None, 'genomic_set_member', type_='foreignkey')
    op.drop_column('genomic_set_member', 'cvl_w1il_pgx_job_run_id')
    op.drop_column('genomic_set_member', 'cvl_w1il_hdr_job_run_id')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

