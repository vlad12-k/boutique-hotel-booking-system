from decimal import Decimal

import pytest
from sqlalchemy import inspect, text
from sqlalchemy.exc import DBAPIError

from hotel_app import create_app
from hotel_app.extensions import db


def test_initial_migration_builds_preserved_schema(tmp_path):
    database_path = tmp_path / "migration.db"
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "synthetic-test-secret",
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path}",
        }
    )

    result = app.test_cli_runner().invoke(args=["db", "upgrade"])
    assert result.exit_code == 0, result.output

    with app.app_context():
        assert set(inspect(db.engine).get_table_names()) == {
            "alembic_version",
            "booking",
            "booking_event",
            "guest",
            "notification_log",
            "payment",
            "room",
            "room_type",
            "security_audit_event",
            "staff_account",
        }


def test_operational_migration_preserves_legacy_rows(tmp_path):
    database_path = tmp_path / "legacy-upgrade.db"
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "synthetic-test-secret",
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path}",
        }
    )
    runner = app.test_cli_runner()
    result = runner.invoke(args=["db", "upgrade", "20260916_0002"])
    assert result.exit_code == 0, result.output

    with app.app_context(), db.engine.begin() as connection:
        connection.execute(
            text(
                """
                INSERT INTO guest (id, full_name, email, phone)
                VALUES (1, 'Synthetic Legacy Guest', 'legacy@example.com', '+0000')
                """
            )
        )
        connection.execute(
            text(
                """
                INSERT INTO room
                    (id, room_number, room_type, price_per_night, status)
                VALUES (1, 'L-1', 'Legacy Double', 99.95, 'Occupied')
                """
            )
        )
        connection.execute(
            text(
                """
                INSERT INTO booking (
                    id, guest_id, room_id, check_in_date, check_out_date,
                    status, total_price, created_at
                ) VALUES (
                    1, 1, 1, '2026-09-16', '2026-09-18',
                    'Checked-in', 199.90, CURRENT_TIMESTAMP
                )
                """
            )
        )

    result = runner.invoke(args=["db", "upgrade"])
    assert result.exit_code == 0, result.output

    with app.app_context(), db.engine.connect() as connection:
        room = connection.execute(
            text(
                """
                SELECT room_number, price_per_night, currency, operational_state,
                       room_type.display_name
                FROM room JOIN room_type ON room.room_type_id = room_type.id
                WHERE room.id = 1
                """
            )
        ).one()
        booking = connection.execute(
            text(
                """
                SELECT total_price, currency, source
                FROM booking WHERE id = 1
                """
            )
        ).one()
        event = connection.execute(
            text(
                """
                SELECT event_type, to_status, to_room_id
                FROM booking_event WHERE booking_id = 1
                """
            )
        ).one()

        assert room == ("L-1", 99.95, "GBP", "ready", "Legacy Double")
        assert booking == (199.9, "GBP", "other")
        assert event == ("legacy_migrated", "Checked-in", 1)

        with pytest.raises(DBAPIError, match="append-only"):
            connection.execute(
                text("UPDATE booking_event SET event_type = 'modified' WHERE id = 1")
            )

    with app.app_context():
        columns = {column["name"]: column for column in inspect(db.engine).get_columns("booking")}
        assert columns["total_price"]["type"].scale == 2


def test_operational_migration_allows_missing_guest_contacts(tmp_path):
    database_path = tmp_path / "optional-contacts.db"
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "synthetic-test-secret",
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path}",
        }
    )
    result = app.test_cli_runner().invoke(args=["db", "upgrade"])
    assert result.exit_code == 0, result.output

    with app.app_context(), db.engine.begin() as connection:
        connection.execute(
            text("INSERT INTO guest (full_name) VALUES ('Synthetic Walk-in')")
        )
        row = connection.execute(
            text("SELECT email, phone FROM guest WHERE full_name = 'Synthetic Walk-in'")
        ).one()
        assert row == (None, None)
