"""add deleted flag for genomic metrics

Revision ID: ce0d4837ba00
Revises: a41c2f2266cb
Create Date: 2021-02-17 13:31:28.006077

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
revision = 'ce0d4837ba00'
down_revision = 'a41c2f2266cb'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()



def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('genomic_gc_validation_metrics', sa.Column('crai_deleted', sa.SmallInteger(), nullable=False))
    op.add_column('genomic_gc_validation_metrics', sa.Column('cram_deleted', sa.SmallInteger(), nullable=False))
    op.add_column('genomic_gc_validation_metrics', sa.Column('cram_md5_deleted', sa.SmallInteger(), nullable=False))
    op.add_column('genomic_gc_validation_metrics', sa.Column('hf_vcf_deleted', sa.SmallInteger(), nullable=False))
    op.add_column('genomic_gc_validation_metrics', sa.Column('hf_vcf_md5_deleted', sa.SmallInteger(), nullable=False))
    op.add_column('genomic_gc_validation_metrics', sa.Column('hf_vcf_tbi_deleted', sa.SmallInteger(), nullable=False))
    op.add_column('genomic_gc_validation_metrics', sa.Column('idat_green_deleted', sa.SmallInteger(), nullable=False))
    op.add_column('genomic_gc_validation_metrics', sa.Column('idat_green_md5_deleted', sa.SmallInteger(), nullable=False))
    op.add_column('genomic_gc_validation_metrics', sa.Column('idat_red_deleted', sa.SmallInteger(), nullable=False))
    op.add_column('genomic_gc_validation_metrics', sa.Column('idat_red_md5_deleted', sa.SmallInteger(), nullable=False))
    op.add_column('genomic_gc_validation_metrics', sa.Column('raw_vcf_deleted', sa.SmallInteger(), nullable=False))
    op.add_column('genomic_gc_validation_metrics', sa.Column('raw_vcf_md5_deleted', sa.SmallInteger(), nullable=False))
    op.add_column('genomic_gc_validation_metrics', sa.Column('raw_vcf_tbi_deleted', sa.SmallInteger(), nullable=False))
    op.add_column('genomic_gc_validation_metrics', sa.Column('vcf_deleted', sa.SmallInteger(), nullable=False))
    op.add_column('genomic_gc_validation_metrics', sa.Column('vcf_md5_deleted', sa.SmallInteger(), nullable=False))
    op.add_column('genomic_gc_validation_metrics', sa.Column('vcf_tbi_deleted', sa.SmallInteger(), nullable=False))
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('genomic_gc_validation_metrics', 'vcf_tbi_deleted')
    op.drop_column('genomic_gc_validation_metrics', 'vcf_md5_deleted')
    op.drop_column('genomic_gc_validation_metrics', 'vcf_deleted')
    op.drop_column('genomic_gc_validation_metrics', 'raw_vcf_tbi_deleted')
    op.drop_column('genomic_gc_validation_metrics', 'raw_vcf_md5_deleted')
    op.drop_column('genomic_gc_validation_metrics', 'raw_vcf_deleted')
    op.drop_column('genomic_gc_validation_metrics', 'idat_red_md5_deleted')
    op.drop_column('genomic_gc_validation_metrics', 'idat_red_deleted')
    op.drop_column('genomic_gc_validation_metrics', 'idat_green_md5_deleted')
    op.drop_column('genomic_gc_validation_metrics', 'idat_green_deleted')
    op.drop_column('genomic_gc_validation_metrics', 'hf_vcf_tbi_deleted')
    op.drop_column('genomic_gc_validation_metrics', 'hf_vcf_md5_deleted')
    op.drop_column('genomic_gc_validation_metrics', 'hf_vcf_deleted')
    op.drop_column('genomic_gc_validation_metrics', 'cram_md5_deleted')
    op.drop_column('genomic_gc_validation_metrics', 'cram_deleted')
    op.drop_column('genomic_gc_validation_metrics', 'crai_deleted')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

