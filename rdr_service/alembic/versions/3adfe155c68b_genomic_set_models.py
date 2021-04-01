"""Genomic Set Models

Revision ID: 3adfe155c68b
Revises: de5a1383d6a1
Create Date: 2019-04-08 10:27:17.052088

"""
import model.utils
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

from rdr_service.model.base import add_table_history_table, drop_table_history_table
from rdr_service.genomic_enums import GenomicSetStatus, GenomicValidationStatus

# revision identifiers, used by Alembic.
revision = "3adfe155c68b"
down_revision = "de5a1383d6a1"
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()


def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "genomic_set",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=True),
        sa.Column("modified", sa.DateTime(), nullable=True),
        sa.Column("genomic_set_name", sa.String(length=80), nullable=False),
        sa.Column("genomic_set_criteria", sa.String(length=80), nullable=False),
        sa.Column("genomic_set_version", sa.Integer(), nullable=False),
        sa.Column("genomic_set_file", sa.String(length=250), nullable=True),
        sa.Column("genomic_set_file_time", sa.DateTime(), nullable=True),
        sa.Column("genomic_set_status", model.utils.Enum(GenomicSetStatus), nullable=True),
        sa.Column("validated_time", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("genomic_set_name", "genomic_set_version", name="uidx_genomic_name_version"),
    )
    op.create_table(
        "genomic_set_member",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=True),
        sa.Column("modified", sa.DateTime(), nullable=True),
        sa.Column("genomic_set_id", sa.Integer(), nullable=False),
        sa.Column("participant_id", sa.Integer(), nullable=False),
        sa.Column("ny_flag", sa.Integer(), nullable=True),
        sa.Column("sex_at_birth", sa.String(length=20), nullable=True),
        sa.Column("genome_type", sa.String(length=80), nullable=True),
        sa.Column("biobank_order_id", sa.String(length=80), nullable=True),
        sa.Column("validation_status", model.utils.Enum(GenomicValidationStatus), nullable=True),
        sa.Column("validated_time", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["biobank_order_id"], ["biobank_order.biobank_order_id"]),
        sa.ForeignKeyConstraint(["genomic_set_id"], ["genomic_set.id"]),
        sa.ForeignKeyConstraint(["participant_id"], ["participant.participant_id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("biobank_order_id"),
    )

    op.alter_column(
        "genomic_set",
        "created",
        existing_type=mysql.DATETIME(fsp=6),
        nullable=True,
        existing_server_default=sa.text("current_timestamp(6)"),
    )
    op.alter_column(
        "genomic_set",
        "modified",
        existing_type=mysql.DATETIME(fsp=6),
        nullable=True,
        existing_server_default=sa.text("current_timestamp(6) ON UPDATE current_timestamp(6)"),
    )

    op.alter_column(
        "genomic_set_member",
        "created",
        existing_type=mysql.DATETIME(fsp=6),
        nullable=True,
        existing_server_default=sa.text("current_timestamp(6)"),
    )
    op.alter_column(
        "genomic_set_member",
        "modified",
        existing_type=mysql.DATETIME(fsp=6),
        nullable=True,
        existing_server_default=sa.text("current_timestamp(6) ON UPDATE current_timestamp(6)"),
    )

    op.alter_column(
        "biobank_dv_order",
        "created",
        existing_type=mysql.DATETIME(fsp=6),
        nullable=True,
        existing_server_default=sa.text("current_timestamp(6)"),
    )
    op.alter_column(
        "biobank_dv_order",
        "modified",
        existing_type=mysql.DATETIME(fsp=6),
        nullable=True,
        existing_server_default=sa.text("current_timestamp(6) ON UPDATE current_timestamp(6)"),
    )
    # ### end Alembic commands ###

    add_table_history_table("genomic_set", op)
    op.execute("""call sp_drop_index_if_exists('genomic_set_history', 'uidx_genomic_name_version')""")

    add_table_history_table("genomic_set_member", op)
    op.execute("""call sp_drop_index_if_exists('genomic_set_member_history', 'biobank_order_id')""")
    op.execute("""call sp_drop_index_if_exists('genomic_set_member_history', 'participant_id')""")
    op.execute("""call sp_drop_index_if_exists('genomic_set_member_history', 'genomic_set_id')""")


def downgrade_rdr():

    drop_table_history_table("genomic_set", op)
    drop_table_history_table("genomic_set_member", op)

    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "genomic_set",
        "modified",
        existing_type=mysql.DATETIME(fsp=6),
        nullable=False,
        existing_server_default=sa.text("current_timestamp(6) ON UPDATE current_timestamp(6)"),
    )
    op.alter_column(
        "genomic_set",
        "created",
        existing_type=mysql.DATETIME(fsp=6),
        nullable=False,
        existing_server_default=sa.text("current_timestamp(6)"),
    )

    op.alter_column(
        "genomic_set_member",
        "modified",
        existing_type=mysql.DATETIME(fsp=6),
        nullable=False,
        existing_server_default=sa.text("current_timestamp(6) ON UPDATE current_timestamp(6)"),
    )
    op.alter_column(
        "genomic_set_member",
        "created",
        existing_type=mysql.DATETIME(fsp=6),
        nullable=False,
        existing_server_default=sa.text("current_timestamp(6)"),
    )

    op.alter_column(
        "biobank_dv_order",
        "modified",
        existing_type=mysql.DATETIME(fsp=6),
        nullable=False,
        existing_server_default=sa.text("current_timestamp(6) ON UPDATE current_timestamp(6)"),
    )
    op.alter_column(
        "biobank_dv_order",
        "created",
        existing_type=mysql.DATETIME(fsp=6),
        nullable=False,
        existing_server_default=sa.text("current_timestamp(6)"),
    )

    op.drop_table("genomic_set_member")
    op.drop_table("genomic_set")
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
