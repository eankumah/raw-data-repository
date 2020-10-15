"""add upload_date to genomic_file_processed

Revision ID: 4d7e99e7b5b4
Revises: 139de0f907dc
Create Date: 2020-10-14 16:59:03.404271

"""
from alembic import op
import sqlalchemy as sa
import rdr_service.model.utils

# revision identifiers, used by Alembic.
revision = '4d7e99e7b5b4'
down_revision = '139de0f907dc'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()


def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('genomic_file_processed', sa.Column('upload_date', rdr_service.model.utils.UTCDateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('genomic_file_processed', 'upload_date')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

