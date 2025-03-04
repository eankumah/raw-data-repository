"""add_hpro_consent_model

Revision ID: bea603bc7568
Revises: b54f52bb5fc5, 56c49230d778
Create Date: 2021-09-10 14:08:17.729954

"""
from alembic import op
import sqlalchemy as sa
import rdr_service.model.utils

# revision identifiers, used by Alembic.
revision = 'bea603bc7568'
down_revision = ('b54f52bb5fc5', '56c49230d778')
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()


def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hpro_consent_files',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created', rdr_service.model.utils.UTCDateTime(), nullable=True),
    sa.Column('modified', rdr_service.model.utils.UTCDateTime(), nullable=True),
    sa.Column('participant_id', sa.Integer(), nullable=True),
    sa.Column('consent_file_id', sa.Integer(), nullable=True),
    sa.Column('file_upload_time', rdr_service.model.utils.UTCDateTime(), nullable=True),
    sa.Column('file_path', sa.String(length=250), nullable=True),
    sa.ForeignKeyConstraint(['consent_file_id'], ['consent_file.id'], ),
    sa.ForeignKeyConstraint(['participant_id'], ['participant.participant_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('hpro_consent_files')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

