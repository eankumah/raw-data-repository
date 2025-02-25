"""genomic_set_member_history_table

Revision ID: 953dbc0cd623
Revises: fc1eb86aa8f4, 355854d777d3
Create Date: 2021-06-29 13:45:37.193972

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '953dbc0cd623'
down_revision = ('fc1eb86aa8f4', '355854d777d3')
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()


def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('genomic_set_member_history', sa.Column('aw2f_manifest_job_run_id', sa.Integer(), nullable=True))
    op.drop_column('genomic_set_member_history', 'aw2f_file_processed_id')
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('genomic_set_member_history', sa.Column('aw2f_file_processed_id', sa.Integer(), nullable=True))
    op.drop_column('genomic_set_member_history', 'aw2f_manifest_job_run_id')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

