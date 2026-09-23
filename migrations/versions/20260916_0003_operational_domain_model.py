"""Add the operational domain model and preserve legacy academic records.

Revision ID: 20260916_0003
Revises: 20260916_0002
Create Date: 2026-09-16
"""

from alembic import op
import sqlalchemy as sa


revision = "20260916_0003"
down_revision = "20260916_0002"
branch_labels = None
depends_on = None


def _create_append_only_guards() -> None:
    dialect = op.get_bind().dialect.name
    if dialect == "postgresql":
        op.execute(
            """
            CREATE FUNCTION prevent_booking_event_mutation()
            RETURNS trigger AS $$
            BEGIN
                RAISE EXCEPTION 'booking_event rows are append-only';
            END;
            $$ LANGUAGE plpgsql
            """
        )
        op.execute(
            """
            CREATE TRIGGER booking_event_no_update
            BEFORE UPDATE ON booking_event
            FOR EACH ROW EXECUTE FUNCTION prevent_booking_event_mutation()
            """
        )
        op.execute(
            """
            CREATE TRIGGER booking_event_no_delete
            BEFORE DELETE ON booking_event
            FOR EACH ROW EXECUTE FUNCTION prevent_booking_event_mutation()
            """
        )
    elif dialect == "sqlite":
        op.execute(
            """
            CREATE TRIGGER booking_event_no_update
            BEFORE UPDATE ON booking_event
            BEGIN
                SELECT RAISE(ABORT, 'booking_event rows are append-only');
            END
            """
        )
        op.execute(
            """
            CREATE TRIGGER booking_event_no_delete
            BEFORE DELETE ON booking_event
            BEGIN
                SELECT RAISE(ABORT, 'booking_event rows are append-only');
            END
            """
        )


def _drop_append_only_guards() -> None:
    dialect = op.get_bind().dialect.name
    op.execute("DROP TRIGGER IF EXISTS booking_event_no_update ON booking_event" if dialect == "postgresql" else "DROP TRIGGER IF EXISTS booking_event_no_update")
    op.execute("DROP TRIGGER IF EXISTS booking_event_no_delete ON booking_event" if dialect == "postgresql" else "DROP TRIGGER IF EXISTS booking_event_no_delete")
    if dialect == "postgresql":
        op.execute("DROP FUNCTION IF EXISTS prevent_booking_event_mutation()")


def upgrade() -> None:
    connection = op.get_bind()

    op.create_table(
        "room_type",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("display_name", sa.String(length=100), nullable=False),
        sa.Column("bathroom_type", sa.String(length=20), nullable=False),
        sa.Column("has_balcony_or_terrace", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "bathroom_type IN ('private', 'shared', 'unspecified')",
            name="ck_room_type_bathroom_type",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )

    op.add_column("room", sa.Column("room_type_id", sa.Integer(), nullable=True))
    op.add_column(
        "room", sa.Column("operational_state", sa.String(length=20), nullable=True)
    )
    op.add_column("room", sa.Column("currency", sa.String(length=3), nullable=True))

    legacy_room_types = connection.execute(
        sa.text("SELECT DISTINCT room_type FROM room ORDER BY room_type")
    ).fetchall()
    for index, row in enumerate(legacy_room_types, start=1):
        connection.execute(
            sa.text(
                """
                INSERT INTO room_type
                    (code, display_name, bathroom_type, has_balcony_or_terrace, is_active, created_at)
                VALUES
                    (:code, :label, 'unspecified', false, true, CURRENT_TIMESTAMP)
                """
            ),
            {"code": f"legacy-{index}", "label": row[0]},
        )
        connection.execute(
            sa.text(
                """
                UPDATE room
                SET room_type_id = (
                    SELECT id FROM room_type WHERE code = :code
                )
                WHERE room_type = :label
                """
            ),
            {"code": f"legacy-{index}", "label": row[0]},
        )

    connection.execute(
        sa.text(
            """
            UPDATE room
            SET operational_state = CASE
                WHEN status = 'Cleaning' THEN 'cleaning'
                WHEN status = 'Maintenance' THEN 'maintenance'
                ELSE 'ready'
            END,
            currency = 'GBP'
            """
        )
    )

    with op.batch_alter_table("room") as batch_op:
        batch_op.alter_column("room_type_id", nullable=False)
        batch_op.alter_column("operational_state", nullable=False)
        batch_op.alter_column("currency", nullable=False)
        batch_op.alter_column(
            "price_per_night",
            existing_type=sa.Float(),
            type_=sa.Numeric(12, 2),
            existing_nullable=False,
            postgresql_using="round(price_per_night::numeric, 2)",
        )
        batch_op.drop_column("room_type")
        batch_op.drop_column("status")
        batch_op.create_foreign_key(
            "fk_room_room_type_id_room_type", "room_type", ["room_type_id"], ["id"]
        )
        batch_op.create_check_constraint(
            "ck_room_non_negative_price", "price_per_night >= 0"
        )
        batch_op.create_check_constraint(
            "ck_room_currency", "length(currency) = 3 AND currency = upper(currency)"
        )
        batch_op.create_check_constraint(
            "ck_room_operational_state",
            "operational_state IN ('ready', 'cleaning', 'maintenance')",
        )

    with op.batch_alter_table("guest") as batch_op:
        batch_op.alter_column(
            "email",
            existing_type=sa.String(length=120),
            type_=sa.String(length=254),
            existing_nullable=False,
            nullable=True,
        )
        batch_op.alter_column(
            "phone", existing_type=sa.String(length=30), nullable=True
        )

    op.add_column("booking", sa.Column("source", sa.String(length=20), nullable=True))
    op.add_column(
        "booking", sa.Column("external_provider", sa.String(length=50), nullable=True)
    )
    op.add_column(
        "booking", sa.Column("external_reference", sa.String(length=120), nullable=True)
    )
    op.add_column("booking", sa.Column("currency", sa.String(length=3), nullable=True))
    connection.execute(sa.text("UPDATE booking SET source = 'other', currency = 'GBP'"))

    with op.batch_alter_table("booking") as batch_op:
        batch_op.alter_column("source", nullable=False)
        batch_op.alter_column("currency", nullable=False)
        batch_op.alter_column(
            "total_price",
            existing_type=sa.Float(),
            type_=sa.Numeric(12, 2),
            existing_nullable=False,
            postgresql_using="round(total_price::numeric, 2)",
        )
        batch_op.create_check_constraint(
            "ck_booking_currency",
            "length(currency) = 3 AND currency = upper(currency)",
        )
        batch_op.create_check_constraint(
            "ck_booking_source",
            "source IN ('direct', 'phone', 'walk_in', 'booking_com', 'other')",
        )
        batch_op.create_check_constraint(
            "ck_booking_status",
            "status IN ('Pending', 'Confirmed', 'Rejected', 'Checked-in', "
            "'Checked-out', 'Cancelled')",
        )
        batch_op.create_check_constraint(
            "ck_booking_external_reference_pair",
            "(external_provider IS NULL AND external_reference IS NULL) OR "
            "(external_provider IS NOT NULL AND external_reference IS NOT NULL)",
        )
        batch_op.create_unique_constraint(
            "uq_booking_external_reference",
            ["external_provider", "external_reference"],
        )

    op.create_table(
        "booking_event",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("booking_id", sa.Integer(), nullable=False),
        sa.Column("event_type", sa.String(length=30), nullable=False),
        sa.Column("from_status", sa.String(length=20), nullable=True),
        sa.Column("to_status", sa.String(length=20), nullable=True),
        sa.Column("from_room_id", sa.Integer(), nullable=True),
        sa.Column("to_room_id", sa.Integer(), nullable=True),
        sa.Column("actor_staff_account_id", sa.Integer(), nullable=True),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "event_type IN ('created', 'modified', 'confirmed', 'rejected', "
            "'cancelled', 'room_reassigned', 'checked_in', 'checked_out', "
            "'legacy_migrated')",
            name="ck_booking_event_type",
        ),
        sa.ForeignKeyConstraint(["booking_id"], ["booking.id"]),
        sa.ForeignKeyConstraint(["from_room_id"], ["room.id"]),
        sa.ForeignKeyConstraint(["to_room_id"], ["room.id"]),
        sa.ForeignKeyConstraint(
            ["actor_staff_account_id"], ["staff_account.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_booking_event_booking_occurred",
        "booking_event",
        ["booking_id", "occurred_at"],
    )
    connection.execute(
        sa.text(
            """
            INSERT INTO booking_event
                (booking_id, event_type, to_status, to_room_id, occurred_at)
            SELECT id, 'legacy_migrated', status, room_id, created_at
            FROM booking
            """
        )
    )

    op.create_table(
        "payment",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("booking_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("external_provider", sa.String(length=50), nullable=True),
        sa.Column("external_reference", sa.String(length=120), nullable=True),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("amount >= 0", name="ck_payment_non_negative_amount"),
        sa.CheckConstraint(
            "length(currency) = 3 AND currency = upper(currency)",
            name="ck_payment_currency",
        ),
        sa.CheckConstraint(
            "status IN ('unpaid', 'deposit_due', 'deposit_paid', "
            "'paid_in_full', 'refunded')",
            name="ck_payment_status",
        ),
        sa.CheckConstraint(
            "(external_provider IS NULL AND external_reference IS NULL) OR "
            "(external_provider IS NOT NULL AND external_reference IS NOT NULL)",
            name="ck_payment_external_reference_pair",
        ),
        sa.ForeignKeyConstraint(["booking_id"], ["booking.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "external_provider", "external_reference", name="uq_payment_external_reference"
        ),
    )
    op.create_index(
        "ix_payment_booking_recorded", "payment", ["booking_id", "recorded_at"]
    )
    _create_append_only_guards()


def downgrade() -> None:
    connection = op.get_bind()
    _drop_append_only_guards()
    op.drop_index("ix_payment_booking_recorded", table_name="payment")
    op.drop_table("payment")
    op.drop_index("ix_booking_event_booking_occurred", table_name="booking_event")
    op.drop_table("booking_event")

    with op.batch_alter_table("booking") as batch_op:
        batch_op.drop_constraint("uq_booking_external_reference", type_="unique")
        batch_op.drop_constraint("ck_booking_external_reference_pair", type_="check")
        batch_op.drop_constraint("ck_booking_source", type_="check")
        batch_op.drop_constraint("ck_booking_status", type_="check")
        batch_op.drop_constraint("ck_booking_currency", type_="check")
        batch_op.alter_column(
            "total_price",
            existing_type=sa.Numeric(12, 2),
            type_=sa.Float(),
            existing_nullable=False,
            postgresql_using="total_price::double precision",
        )
        batch_op.drop_column("currency")
        batch_op.drop_column("external_reference")
        batch_op.drop_column("external_provider")
        batch_op.drop_column("source")

    with op.batch_alter_table("guest") as batch_op:
        batch_op.alter_column(
            "email",
            existing_type=sa.String(length=254),
            type_=sa.String(length=120),
            nullable=False,
        )
        batch_op.alter_column(
            "phone", existing_type=sa.String(length=30), nullable=False
        )

    op.add_column("room", sa.Column("room_type", sa.String(length=50), nullable=True))
    op.add_column("room", sa.Column("status", sa.String(length=20), nullable=True))
    connection.execute(
        sa.text(
            """
            UPDATE room
            SET room_type = (
                SELECT display_name FROM room_type WHERE room_type.id = room.room_type_id
            ),
            status = CASE operational_state
                WHEN 'cleaning' THEN 'Cleaning'
                WHEN 'maintenance' THEN 'Maintenance'
                ELSE 'Available'
            END
            """
        )
    )
    with op.batch_alter_table("room") as batch_op:
        batch_op.drop_constraint("fk_room_room_type_id_room_type", type_="foreignkey")
        batch_op.drop_constraint("ck_room_operational_state", type_="check")
        batch_op.drop_constraint("ck_room_currency", type_="check")
        batch_op.drop_constraint("ck_room_non_negative_price", type_="check")
        batch_op.alter_column("room_type", nullable=False)
        batch_op.alter_column("status", nullable=False)
        batch_op.alter_column(
            "price_per_night",
            existing_type=sa.Numeric(12, 2),
            type_=sa.Float(),
            existing_nullable=False,
            postgresql_using="price_per_night::double precision",
        )
        batch_op.drop_column("operational_state")
        batch_op.drop_column("currency")
        batch_op.drop_column("room_type_id")
    op.drop_table("room_type")
