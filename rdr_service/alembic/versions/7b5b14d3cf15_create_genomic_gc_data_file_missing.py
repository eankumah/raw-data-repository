"""create genomic_gc_data_file_missing

Revision ID: 7b5b14d3cf15
Revises: 15b708d94dc6
Create Date: 2021-07-28 14:00:43.087562

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '7b5b14d3cf15'
down_revision = '15b708d94dc6'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()


def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genomic_gc_data_file_missing',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('gc_site_id', sa.String(length=64), nullable=False),
    sa.Column('file_type', sa.String(length=128), nullable=False),
    sa.Column('run_id', sa.Integer(), nullable=False),
    sa.Column('gc_validation_metric_id', sa.Integer(), nullable=False),
    sa.Column('resolved', sa.SmallInteger(), nullable=False),
    sa.Column('resolved_date', sa.DateTime(), nullable=True),
    sa.Column('ignore_flag', sa.SmallInteger(), nullable=False),
    sa.ForeignKeyConstraint(['gc_validation_metric_id'], ['genomic_gc_validation_metrics.id'], ),
    sa.ForeignKeyConstraint(['run_id'], ['genomic_job_run.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_genomic_gc_data_file_missing_file_type'), 'genomic_gc_data_file_missing', ['file_type'], unique=False)
    op.create_index(op.f('ix_genomic_gc_data_file_missing_gc_site_id'), 'genomic_gc_data_file_missing', ['gc_site_id'], unique=False)
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_genomic_gc_data_file_missing_gc_site_id'), table_name='genomic_gc_data_file_missing')
    op.drop_index(op.f('ix_genomic_gc_data_file_missing_file_type'), table_name='genomic_gc_data_file_missing')
    op.drop_table('genomic_gc_data_file_missing')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

