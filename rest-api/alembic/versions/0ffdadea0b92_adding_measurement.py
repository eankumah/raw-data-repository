"""Adding measurement

Revision ID: 0ffdadea0b92
Revises: ffcd82a35890
Create Date: 2017-08-30 17:33:54.104062

"""
from alembic import op
import sqlalchemy as sa
import model.utils


from participant_enums import PhysicalMeasurementsStatus, QuestionnaireStatus
from participant_enums import WithdrawalStatus, SuspensionStatus
from participant_enums import EnrollmentStatus, Race, SampleStatus, OrganizationType
from model.code import CodeType

# revision identifiers, used by Alembic.
revision = '0ffdadea0b92'
down_revision = 'ffcd82a35890'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('measurement',
    sa.Column('measurement_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('physical_measurements_id', sa.Integer(), nullable=False),
    sa.Column('code_system', sa.String(length=255), nullable=False),
    sa.Column('code_value', sa.String(length=255), nullable=False),
    sa.Column('measurement_time', model.utils.UTCDateTime(), nullable=False),
    sa.Column('body_site_code_system', sa.String(length=255), nullable=True),
    sa.Column('body_site_code_value', sa.String(length=255), nullable=True),
    sa.Column('value_string', sa.String(length=1024), nullable=True),
    sa.Column('value_decimal', sa.Float(), nullable=True),
    sa.Column('value_unit', sa.String(length=255), nullable=True),
    sa.Column('value_code_system', sa.String(length=255), nullable=True),
    sa.Column('value_code_value', sa.String(length=255), nullable=True),
    sa.Column('value_datetime', model.utils.UTCDateTime(), nullable=True),
    sa.Column('parent_id', sa.BIGINT(), nullable=True),
    sa.Column('qualifier_id', sa.BIGINT(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['measurement.measurement_id'], ),
    sa.ForeignKeyConstraint(['physical_measurements_id'], ['physical_measurements.physical_measurements_id'], ),
    sa.ForeignKeyConstraint(['qualifier_id'], ['measurement.measurement_id'], ),
    sa.PrimaryKeyConstraint('measurement_id')
    )
    op.create_table('measurement_to_qualifier',
    sa.Column('measurement_id', sa.BIGINT(), nullable=False),
    sa.Column('qualifier_id', sa.BIGINT(), nullable=False),
    sa.ForeignKeyConstraint(['measurement_id'], ['measurement.measurement_id'], ),
    sa.ForeignKeyConstraint(['qualifier_id'], ['measurement.measurement_id'], ),
    sa.PrimaryKeyConstraint('measurement_id', 'qualifier_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('measurement_to_qualifier')
    op.drop_table('measurement')
    # ### end Alembic commands ###
