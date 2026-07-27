from datetime import date

import pytest
from flask import Flask

from models import Booking, Guest, Room, db
from services.booking_service import (
    BookingServiceError,
    cancel_booking,
    check_in_booking,
    check_out_booking,
    create_booking,
)


@pytest.fixture()
def test_app(tmp_path):
    database_path = tmp_path / "test_hotel.db"

    app = Flask(__name__)
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{database_path}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)

    with app.app_context():
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture()
def guest_and_room(test_app):
    with test_app.app_context():
        guest = Guest(
            full_name="Test Guest",
            email="test.guest@example.com",
            phone="07123456789",
            notes="Test fixture guest",
        )

        room = Room(
            room_number="201",
            room_type="Double",
            price_per_night=100.0,
            status="Available",
        )

        db.session.add_all([guest, room])
        db.session.commit()

        return guest.id, room.id


def test_create_booking_calculates_total_price(
    test_app,
    guest_and_room,
):
    guest_id, room_id = guest_and_room

    with test_app.app_context():
        booking = create_booking(
            guest_id=guest_id,
            room_id=room_id,
            check_in_date=date(2026, 8, 10),
            check_out_date=date(2026, 8, 13),
            booking_status="Confirmed",
        )

        db.session.commit()

        assert booking.status == "Confirmed"
        assert booking.total_price == 300.0
        assert booking.guest_id == guest_id
        assert booking.room_id == room_id


def test_create_booking_rejects_invalid_date_range(
    test_app,
    guest_and_room,
):
    guest_id, room_id = guest_and_room

    with test_app.app_context():
        with pytest.raises(
            BookingServiceError,
            match="Check-out date must be after check-in date.",
        ):
            create_booking(
                guest_id=guest_id,
                room_id=room_id,
                check_in_date=date(2026, 8, 10),
                check_out_date=date(2026, 8, 10),
                booking_status="Confirmed",
            )


def test_create_booking_rejects_invalid_initial_status(
    test_app,
    guest_and_room,
):
    guest_id, room_id = guest_and_room

    with test_app.app_context():
        with pytest.raises(
            BookingServiceError,
            match="New bookings can only be Pending or Confirmed.",
        ):
            create_booking(
                guest_id=guest_id,
                room_id=room_id,
                check_in_date=date(2026, 8, 10),
                check_out_date=date(2026, 8, 12),
                booking_status="Checked-in",
            )


def test_create_booking_rejects_invalid_guest(
    test_app,
    guest_and_room,
):
    _, room_id = guest_and_room

    with test_app.app_context():
        with pytest.raises(
            BookingServiceError,
            match="Please select a valid guest and room.",
        ):
            create_booking(
                guest_id=99999,
                room_id=room_id,
                check_in_date=date(2026, 8, 10),
                check_out_date=date(2026, 8, 12),
                booking_status="Confirmed",
            )


def test_create_booking_rejects_invalid_room(
    test_app,
    guest_and_room,
):
    guest_id, _ = guest_and_room

    with test_app.app_context():
        with pytest.raises(
            BookingServiceError,
            match="Please select a valid guest and room.",
        ):
            create_booking(
                guest_id=guest_id,
                room_id=99999,
                check_in_date=date(2026, 8, 10),
                check_out_date=date(2026, 8, 12),
                booking_status="Confirmed",
            )


def test_create_booking_rejects_maintenance_room(
    test_app,
    guest_and_room,
):
    guest_id, room_id = guest_and_room

    with test_app.app_context():
        room = db.session.get(Room, room_id)
        room.status = "Maintenance"
        db.session.commit()

        with pytest.raises(
            BookingServiceError,
            match="Rooms under Maintenance cannot be booked.",
        ):
            create_booking(
                guest_id=guest_id,
                room_id=room_id,
                check_in_date=date(2026, 8, 10),
                check_out_date=date(2026, 8, 12),
                booking_status="Confirmed",
            )


def test_create_booking_rejects_overlapping_booking(
    test_app,
    guest_and_room,
):
    guest_id, room_id = guest_and_room

    with test_app.app_context():
        existing_booking = Booking(
            guest_id=guest_id,
            room_id=room_id,
            check_in_date=date(2026, 8, 10),
            check_out_date=date(2026, 8, 15),
            status="Confirmed",
            total_price=500.0,
        )

        db.session.add(existing_booking)
        db.session.commit()

        with pytest.raises(
            BookingServiceError,
            match="Booking rejected",
        ):
            create_booking(
                guest_id=guest_id,
                room_id=room_id,
                check_in_date=date(2026, 8, 12),
                check_out_date=date(2026, 8, 17),
                booking_status="Confirmed",
            )


def test_create_booking_allows_adjacent_dates(
    test_app,
    guest_and_room,
):
    guest_id, room_id = guest_and_room

    with test_app.app_context():
        existing_booking = Booking(
            guest_id=guest_id,
            room_id=room_id,
            check_in_date=date(2026, 8, 10),
            check_out_date=date(2026, 8, 12),
            status="Confirmed",
            total_price=200.0,
        )

        db.session.add(existing_booking)
        db.session.commit()

        new_booking = create_booking(
            guest_id=guest_id,
            room_id=room_id,
            check_in_date=date(2026, 8, 12),
            check_out_date=date(2026, 8, 14),
            booking_status="Confirmed",
        )

        db.session.commit()

        assert new_booking.check_in_date == date(2026, 8, 12)
        assert new_booking.total_price == 200.0


def test_cancel_booking_changes_status(
    test_app,
    guest_and_room,
):
    guest_id, room_id = guest_and_room

    with test_app.app_context():
        booking = Booking(
            guest_id=guest_id,
            room_id=room_id,
            check_in_date=date(2026, 8, 10),
            check_out_date=date(2026, 8, 12),
            status="Confirmed",
            total_price=200.0,
        )

        db.session.add(booking)
        db.session.commit()

        cancel_booking(booking)
        db.session.commit()

        assert booking.status == "Cancelled"


@pytest.mark.parametrize(
    "blocked_status",
    ["Checked-out", "Cancelled"],
)
def test_cancel_booking_rejects_blocked_statuses(
    test_app,
    guest_and_room,
    blocked_status,
):
    guest_id, room_id = guest_and_room

    with test_app.app_context():
        booking = Booking(
            guest_id=guest_id,
            room_id=room_id,
            check_in_date=date(2026, 8, 10),
            check_out_date=date(2026, 8, 12),
            status=blocked_status,
            total_price=200.0,
        )

        db.session.add(booking)
        db.session.commit()

        with pytest.raises(
            BookingServiceError,
            match="Booking cannot be cancelled in its current status.",
        ):
            cancel_booking(booking)


def test_check_in_booking_updates_booking_and_room_status(
    test_app,
    guest_and_room,
):
    guest_id, room_id = guest_and_room

    with test_app.app_context():
        booking = Booking(
            guest_id=guest_id,
            room_id=room_id,
            check_in_date=date(2026, 8, 10),
            check_out_date=date(2026, 8, 12),
            status="Confirmed",
            total_price=200.0,
        )

        db.session.add(booking)
        db.session.commit()

        check_in_booking(
            booking,
            current_date=date(2026, 8, 10),
        )
        db.session.commit()

        assert booking.status == "Checked-in"
        assert booking.room.status == "Occupied"


def test_check_in_booking_rejects_early_check_in(
    test_app,
    guest_and_room,
):
    guest_id, room_id = guest_and_room

    with test_app.app_context():
        booking = Booking(
            guest_id=guest_id,
            room_id=room_id,
            check_in_date=date(2026, 8, 10),
            check_out_date=date(2026, 8, 12),
            status="Confirmed",
            total_price=200.0,
        )

        db.session.add(booking)
        db.session.commit()

        with pytest.raises(
            BookingServiceError,
            match="Guest cannot be checked in before the check-in date.",
        ):
            check_in_booking(
                booking,
                current_date=date(2026, 8, 9),
            )


def test_check_in_booking_rejects_invalid_status(
    test_app,
    guest_and_room,
):
    guest_id, room_id = guest_and_room

    with test_app.app_context():
        booking = Booking(
            guest_id=guest_id,
            room_id=room_id,
            check_in_date=date(2026, 8, 10),
            check_out_date=date(2026, 8, 12),
            status="Cancelled",
            total_price=200.0,
        )

        db.session.add(booking)
        db.session.commit()

        with pytest.raises(
            BookingServiceError,
            match="Only Pending or Confirmed bookings can be checked in.",
        ):
            check_in_booking(
                booking,
                current_date=date(2026, 8, 10),
            )


def test_check_out_booking_updates_booking_and_room_status(
    test_app,
    guest_and_room,
):
    guest_id, room_id = guest_and_room

    with test_app.app_context():
        room = db.session.get(Room, room_id)
        room.status = "Occupied"

        booking = Booking(
            guest_id=guest_id,
            room_id=room_id,
            check_in_date=date(2026, 8, 10),
            check_out_date=date(2026, 8, 12),
            status="Checked-in",
            total_price=200.0,
        )

        db.session.add(booking)
        db.session.commit()

        check_out_booking(booking)
        db.session.commit()

        assert booking.status == "Checked-out"
        assert booking.room.status == "Cleaning"


def test_check_out_booking_rejects_invalid_status(
    test_app,
    guest_and_room,
):
    guest_id, room_id = guest_and_room

    with test_app.app_context():
        booking = Booking(
            guest_id=guest_id,
            room_id=room_id,
            check_in_date=date(2026, 8, 10),
            check_out_date=date(2026, 8, 12),
            status="Confirmed",
            total_price=200.0,
        )

        db.session.add(booking)
        db.session.commit()

        with pytest.raises(
            BookingServiceError,
            match="Only checked-in bookings can be checked out.",
        ):
            check_out_booking(booking)