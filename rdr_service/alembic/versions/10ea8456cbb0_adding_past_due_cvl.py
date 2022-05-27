"""adding_past_due_cvl

Revision ID: 10ea8456cbb0
Revises: d189326d0fc4, 4d2ce3440f21, 4dcc14a0c152
Create Date: 2022-05-27 14:15:09.040230

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '10ea8456cbb0'
down_revision = ('d189326d0fc4', '4d2ce3440f21', '4dcc14a0c152')
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()


def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genomic_cvl_result_past_due',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('genomic_set_member_id', sa.Integer(), nullable=False),
    sa.Column('sample_id', sa.String(length=255), nullable=False),
    sa.Column('results_type', sa.String(length=128), nullable=False),
    sa.Column('cvl_site_id', sa.String(length=128), nullable=False),
    sa.Column('email_notification_sent', sa.SmallInteger(), nullable=False),
    sa.Column('email_notification_sent_date', sa.DateTime(), nullable=True),
    sa.Column('resolved', sa.SmallInteger(), nullable=False),
    sa.Column('resolved_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['genomic_set_member_id'], ['genomic_set_member.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_genomic_cvl_result_past_due_cvl_site_id'), 'genomic_cvl_result_past_due', ['cvl_site_id'], unique=False)
    op.create_index(op.f('ix_genomic_cvl_result_past_due_sample_id'), 'genomic_cvl_result_past_due', ['sample_id'], unique=False)
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_genomic_cvl_result_past_due_sample_id'), table_name='genomic_cvl_result_past_due')
    op.drop_index(op.f('ix_genomic_cvl_result_past_due_cvl_site_id'), table_name='genomic_cvl_result_past_due')
    op.drop_table('genomic_cvl_result_past_due')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

