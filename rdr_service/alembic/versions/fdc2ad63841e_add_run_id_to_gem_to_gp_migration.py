"""add run id to gem_to_gp_migration

Revision ID: fdc2ad63841e
Revises: e902f7b8bc58
Create Date: 2021-10-21 09:31:31.076339

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'fdc2ad63841e'
down_revision = 'e902f7b8bc58'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()


def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('gem_to_gp_migration', sa.Column('run_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'gem_to_gp_migration', 'genomic_job_run', ['run_id'], ['id'])
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'gem_to_gp_migration', type_='foreignkey')
    op.drop_column('gem_to_gp_migration', 'run_id')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

