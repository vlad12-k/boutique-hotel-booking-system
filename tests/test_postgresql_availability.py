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
                INSERT INTO room (room_number, room_type, price_per_night, status)
                VALUES (:number, 'Synthetic', 100, 'Available')
                RETURNING id
                """
            ),
            {"number": f"race-{suffix}"},
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
                        status, total_price, created_at
                    ) VALUES (
                        :guest_id, :room_id, :check_in, :check_out,
                        'Confirmed', 200, CURRENT_TIMESTAMP
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
