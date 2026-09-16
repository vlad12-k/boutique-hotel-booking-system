import os
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from threading import Barrier
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import DBAPIError

from hotel_app import create_app


@pytest.fixture(scope="module")
def postgres_engine():
    database_url = os.getenv("POSTGRES_TEST_DATABASE_URL")
    if not database_url:
        pytest.skip("POSTGRES_TEST_DATABASE_URL is not configured")

    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "synthetic-postgresql-test-secret",
            "SQLALCHEMY_DATABASE_URI": database_url,
        }
    )
    result = app.test_cli_runner().invoke(args=["db", "upgrade"])
    assert result.exit_code == 0, result.output

    engine = create_engine(database_url)
    yield engine
    engine.dispose()


def create_guest_and_room(engine):
    suffix = uuid4().hex[:10]
    with engine.begin() as connection:
        guest_id = connection.execute(
            text(
                """
                INSERT INTO guest (full_name, email, phone)
                VALUES (:name, :email, :phone)
                RETURNING id
                """
            ),
            {
                "name": "Synthetic Concurrency Guest",
                "email": f"concurrency-{suffix}@example.com",
                "phone": "+00000000000",
            },
        ).scalar_one()
        room_id = connection.execute(
            text(
                """
                WITH inserted_type AS (
                    INSERT INTO room_type (
                        code, display_name, bathroom_type, has_balcony_or_terrace,
                        is_active, created_at
                    ) VALUES (
                        :type_code, 'Synthetic', 'private', false,
                        true, CURRENT_TIMESTAMP
                    )
                    RETURNING id
                )
                INSERT INTO room (
                    room_number, room_type_id, price_per_night,
                    currency, operational_state
                )
                SELECT :number, id, 100.00, 'ILS', 'ready'
                FROM inserted_type
                RETURNING id
                """
            ),
            {"number": f"race-{suffix}", "type_code": f"race-{suffix}"},
        ).scalar_one()
    return guest_id, room_id


def insert_booking(engine, barrier, guest_id, room_id, check_in, check_out):
    try:
        with engine.connect() as connection:
            transaction = connection.begin()
            barrier.wait(timeout=10)
            connection.execute(
                text(
                    """
                    INSERT INTO booking (
                        guest_id, room_id, check_in_date, check_out_date,
                        status, source, total_price, currency, created_at
                    ) VALUES (
                        :guest_id, :room_id, :check_in, :check_out,
                        'Confirmed', 'direct', 200.00, 'ILS', CURRENT_TIMESTAMP
                    )
                    """
                ),
                {
                    "guest_id": guest_id,
                    "room_id": room_id,
                    "check_in": check_in,
                    "check_out": check_out,
                },
            )
            transaction.commit()
        return "committed"
    except DBAPIError:
        return "rejected"


@pytest.mark.postgresql
def test_last_room_race_allows_exactly_one_overlapping_booking(postgres_engine):
    guest_id, room_id = create_guest_and_room(postgres_engine)
    barrier = Barrier(2)

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(
                insert_booking,
                postgres_engine,
                barrier,
                guest_id,
                room_id,
                date(2026, 10, 10),
                date(2026, 10, 12),
            )
            for _ in range(2)
        ]

    assert sorted(future.result() for future in futures) == ["committed", "rejected"]


@pytest.mark.postgresql
def test_database_constraint_allows_adjacent_stays(postgres_engine):
    guest_id, room_id = create_guest_and_room(postgres_engine)
    barrier = Barrier(1)

    first = insert_booking(
        postgres_engine,
        barrier,
        guest_id,
        room_id,
        date(2026, 11, 10),
        date(2026, 11, 12),
    )
    second = insert_booking(
        postgres_engine,
        barrier,
        guest_id,
        room_id,
        date(2026, 11, 12),
        date(2026, 11, 14),
    )

    assert (first, second) == ("committed", "committed")


@pytest.mark.postgresql
def test_postgresql_exclusion_constraint_is_installed(postgres_engine):
    with postgres_engine.connect() as connection:
        exists = connection.execute(
            text(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM pg_constraint
                    WHERE conname = 'ex_booking_room_active_stay'
                )
                """
            )
        ).scalar_one()

    assert exists is True


@pytest.mark.postgresql
def test_authentication_tables_and_constraints_are_installed(postgres_engine):
    with postgres_engine.connect() as connection:
        tables = connection.execute(
            text(
                """
                SELECT tablename
                FROM pg_tables
                WHERE schemaname = 'public'
                  AND tablename IN ('staff_account', 'security_audit_event')
                """
            )
        ).scalars()
        constraints = connection.execute(
            text(
                """
                SELECT conname
                FROM pg_constraint
                WHERE conname IN (
                    'ck_staff_account_email_normalised',
                    'ck_staff_account_role'
                )
                """
            )
        ).scalars()

    assert set(tables) == {"security_audit_event", "staff_account"}
    assert set(constraints) == {
        "ck_staff_account_email_normalised",
        "ck_staff_account_role",
    }


@pytest.mark.postgresql
def test_operational_domain_schema_is_installed(postgres_engine):
    with postgres_engine.connect() as connection:
        tables = set(
            connection.execute(
                text(
                    """
                    SELECT tablename
                    FROM pg_tables
                    WHERE schemaname = 'public'
                      AND tablename IN ('room_type', 'booking_event', 'payment')
                    """
                )
            ).scalars()
        )
        money_columns = connection.execute(
            text(
                """
                SELECT table_name, column_name, numeric_precision, numeric_scale
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND (table_name, column_name) IN (
                      ('room', 'price_per_night'),
                      ('booking', 'total_price'),
                      ('payment', 'amount')
                  )
                ORDER BY table_name, column_name
                """
            )
        ).all()
        constraints = set(
            connection.execute(
                text(
                    """
                    SELECT conname
                    FROM pg_constraint
                    WHERE conname IN (
                        'ck_room_operational_state',
                        'ck_booking_source',
                        'ck_booking_status',
                        'uq_booking_external_reference',
                        'ck_payment_status'
                    )
                    """
                )
            ).scalars()
        )

    assert tables == {"room_type", "booking_event", "payment"}
    assert money_columns == [
        ("booking", "total_price", 12, 2),
        ("payment", "amount", 12, 2),
        ("room", "price_per_night", 12, 2),
    ]
    assert constraints == {
        "ck_room_operational_state",
        "ck_booking_source",
        "ck_booking_status",
        "uq_booking_external_reference",
        "ck_payment_status",
    }


@pytest.mark.postgresql
def test_booking_event_database_trigger_rejects_mutation(postgres_engine):
    guest_id, room_id = create_guest_and_room(postgres_engine)
    with postgres_engine.begin() as connection:
        booking_id = connection.execute(
            text(
                """
                INSERT INTO booking (
                    guest_id, room_id, check_in_date, check_out_date,
                    status, source, total_price, currency, created_at
                ) VALUES (
                    :guest_id, :room_id, '2027-02-01', '2027-02-02',
                    'Confirmed', 'direct', 100.00, 'ILS', CURRENT_TIMESTAMP
                )
                RETURNING id
                """
            ),
            {"guest_id": guest_id, "room_id": room_id},
        ).scalar_one()
        event_id = connection.execute(
            text(
                """
                INSERT INTO booking_event (
                    booking_id, event_type, to_status, to_room_id, occurred_at
                ) VALUES (
                    :booking_id, 'created', 'Confirmed', :room_id,
                    CURRENT_TIMESTAMP
                )
                RETURNING id
                """
            ),
            {"booking_id": booking_id, "room_id": room_id},
        ).scalar_one()

    with pytest.raises(DBAPIError, match="append-only"):
        with postgres_engine.begin() as connection:
            connection.execute(
                text(
                    "UPDATE booking_event SET event_type = 'modified' WHERE id = :id"
                ),
                {"id": event_id},
            )
