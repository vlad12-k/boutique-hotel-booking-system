"""Create the preserved academic schema with production database protections.

Revision ID: 20260916_0001
Revises:
Create Date: 2026-09-16
"""

from alembic import op
import sqlalchemy as sa


revision = "20260916_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "guest",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False),
        sa.Column("phone", sa.String(length=30), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "room",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_number", sa.String(length=20), nullable=False),
        sa.Column("room_type", sa.String(length=50), nullable=False),
        sa.Column("price_per_night", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("room_number"),
    )
    op.create_table(
        "booking",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("guest_id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("check_in_date", sa.Date(), nullable=False),
        sa.Column("check_out_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("total_price", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "check_out_date > check_in_date",
            name="ck_booking_valid_stay_period",
        ),
        sa.CheckConstraint(
            "total_price >= 0",
            name="ck_booking_non_negative_total",
        ),
        sa.ForeignKeyConstraint(["guest_id"], ["guest.id"]),
        sa.ForeignKeyConstraint(["room_id"], ["room.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_booking_room_dates",
        "booking",
        ["room_id", "check_in_date", "check_out_date"],
    )
    op.create_table(
        "notification_log",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=True),
        sa.Column("booking_id", sa.Integer(), nullable=True),
        sa.Column("channel", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["booking_id"], ["booking.id"]),
        sa.ForeignKeyConstraint(["room_id"], ["room.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    if op.get_bind().dialect.name == "postgresql":
        op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")
        op.execute(
            """
            ALTER TABLE booking
            ADD CONSTRAINT ex_booking_room_active_stay
            EXCLUDE USING gist (
                room_id WITH =,
                daterange(check_in_date, check_out_date, '[)') WITH &&
            )
            WHERE (status IN ('Pending', 'Confirmed', 'Checked-in'))
            """
        )


def downgrade() -> None:
    op.drop_table("notification_log")
    op.drop_index("ix_booking_room_dates", table_name="booking")
    op.drop_table("booking")
    op.drop_table("room")
    op.drop_table("guest")
