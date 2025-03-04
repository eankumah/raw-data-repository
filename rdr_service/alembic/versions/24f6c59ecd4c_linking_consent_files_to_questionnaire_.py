"""linking consent files to questionnaire responses

Revision ID: 24f6c59ecd4c
Revises: ee2270c92d0e
Create Date: 2022-01-26 14:16:02.633457

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
from rdr_service.model.consent_file import ConsentType
from rdr_service.model.site_enums import SiteStatus, EnrollingStatus, DigitalSchedulingStatus, ObsoleteStatus

# revision identifiers, used by Alembic.
revision = '24f6c59ecd4c'
down_revision = 'ee2270c92d0e'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()



def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('consent_response',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created', rdr_service.model.utils.UTCDateTime(), nullable=True),
        sa.Column('questionnaire_response_id', sa.Integer(), nullable=False),
        sa.Column('type', rdr_service.model.utils.Enum(ConsentType), nullable=True),
        sa.ForeignKeyConstraint(['questionnaire_response_id'], ['questionnaire_response.questionnaire_response_id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.add_column('consent_file', sa.Column('consent_response_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'consent_file', 'consent_response', ['consent_response_id'], ['id'])
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'consent_file', type_='foreignkey')
    op.drop_column('consent_file', 'consent_response_id')
    op.drop_table('consent_response')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

