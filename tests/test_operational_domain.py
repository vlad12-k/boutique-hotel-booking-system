from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy.exc import IntegrityError

from hotel_app.inventory import HAIFA_ROOMS
from hotel_app.models import (
    Booking,
    BookingEvent,
    Guest,
    Payment,
    Room,
    RoomType,
    db,
)
from services.booking_service import (
    BookingServiceError,
    cancel_booking,
    check_in_booking,
    check_out_booking,
    confirm_booking,
    create_booking,
    reject_booking,
    reassign_booking_room,
)


def create_guest_and_room(
    *,
    room_number="1",
    rate=Decimal("100.00"),
    currency="ILS",
):
    guest = Guest(full_name="Synthetic Guest")
    room_type = RoomType(
        code=f"synthetic-{room_number}",
        display_name="Configurable synthetic room",
        bathroom_type="private",
    )
    room = Room(
        room_number=room_number,
        room_type=room_type,
        price_per_night=rate,
        currency=currency,
        operational_state="ready",
    )
    db.session.add_all([guest, room_type, room])
    db.session.commit()
    return guest, room


def test_production_inventory_contract_has_exact_physical_rooms():
    assert [(room.number, room.room_type_code) for room in HAIFA_ROOMS] == [
        ("1", "private-bathroom"),
        ("2", "private-bathroom"),
        ("3", "private-bathroom-terrace"),
        ("4", "shared-bathroom-economy"),
        ("5", "shared-bathroom-economy"),
        ("6", "private-bathroom"),
        ("7", "private-bathroom"),
    ]


def test_production_seed_requires_configured_rates(application):
    result = application.test_cli_runner().invoke(args=["seed-haifa-inventory"])
    assert result.exit_code != 0
    assert "HAIFA_PRIVATE_ROOM_RATE must be configured" in result.output


def test_production_seed_is_configurable_and_exact(application):
    application.config.update(
        PROPERTY_CURRENCY="ILS",
        HAIFA_PRIVATE_ROOM_LABEL="Configured private",
        HAIFA_TERRACE_ROOM_LABEL="Configured terrace",
        HAIFA_ECONOMY_ROOM_LABEL="Configured economy",
        HAIFA_PRIVATE_ROOM_RATE="410.10",
        HAIFA_TERRACE_ROOM_RATE="510.20",
        HAIFA_ECONOMY_ROOM_RATE="310.30",
    )

    result = application.test_cli_runner().invoke(args=["seed-haifa-inventory"])
    assert result.exit_code == 0, result.output

    with application.app_context():
        rooms = Room.query.order_by(Room.room_number).all()
        assert [room.room_number for room in rooms] == [str(i) for i in range(1, 8)]
        assert [room.room_type.bathroom_type for room in rooms] == [
            "private",
            "private",
            "private",
            "shared",
            "shared",
            "private",
            "private",
        ]
        assert rooms[2].room_type.has_balcony_or_terrace is True
        assert all(room.currency == "ILS" for room in rooms)
        assert rooms[0].price_per_night == Decimal("410.10")


def test_academic_seed_remains_explicit_and_separate(application):
    result = application.test_cli_runner().invoke(args=["seed-academic-demo"])
    assert result.exit_code == 0, result.output

    with application.app_context():
        assert Room.query.count() == 10
        assert RoomType.query.count() == 5
        assert {room.currency for room in Room.query.all()} == {"GBP"}


def test_guest_contact_fields_are_optional(application):
    with application.app_context():
        guest = Guest(full_name="Walk-in Guest")
        db.session.add(guest)
        db.session.commit()
        assert guest.email is None
        assert guest.phone is None


def test_money_uses_decimal_and_booking_currency_snapshot(application):
    with application.app_context():
        guest, room = create_guest_and_room(rate=Decimal("0.10"))
        booking = create_booking(
            guest.id,
            room.id,
            date(2026, 10, 1),
            date(2026, 10, 4),
            "Confirmed",
            source="phone",
        )
        db.session.commit()

        assert booking.total_price == Decimal("0.30")
        assert booking.currency == "ILS"
        assert [event.event_type for event in booking.events] == [
            "created",
            "confirmed",
        ]


def test_external_reservation_reference_is_an_idempotency_boundary(application):
    with application.app_context():
        guest, room = create_guest_and_room()
        create_booking(
            guest.id,
            room.id,
            date(2026, 10, 1),
            date(2026, 10, 2),
            "Confirmed",
            source="booking_com",
            external_provider="synthetic-provider",
            external_reference="synthetic-reference",
        )
        db.session.commit()

        with pytest.raises(BookingServiceError, match="already recorded"):
            create_booking(
                guest.id,
                room.id,
                date(2026, 10, 2),
                date(2026, 10, 3),
                "Confirmed",
                source="booking_com",
                external_provider="synthetic-provider",
                external_reference="synthetic-reference",
            )


def test_occupancy_is_derived_and_readiness_remains_separate(application):
    with application.app_context():
        guest, room = create_guest_and_room()
        booking = create_booking(
            guest.id,
            room.id,
            date(2026, 10, 1),
            date(2026, 10, 2),
            "Confirmed",
        )
        db.session.commit()

        check_in_booking(booking, current_date=date(2026, 10, 1))
        db.session.commit()
        assert room.operational_state == "ready"
        assert room.status == "Occupied"

        check_out_booking(booking)
        db.session.commit()
        assert room.operational_state == "cleaning"
        assert room.status == "Cleaning"


def test_booking_lifecycle_and_room_reassignment_are_audited(application):
    with application.app_context():
        guest, first_room = create_guest_and_room(room_number="1")
        second_type = RoomType(
            code="synthetic-2",
            display_name="Second type",
            bathroom_type="shared",
        )
        second_room = Room(
            room_number="2",
            room_type=second_type,
            price_per_night=Decimal("80.00"),
            currency="ILS",
            operational_state="ready",
        )
        db.session.add_all([second_type, second_room])
        db.session.commit()

        booking = create_booking(
            guest.id,
            first_room.id,
            date(2026, 11, 1),
            date(2026, 11, 3),
            "Pending",
        )
        db.session.flush()
        reassign_booking_room(booking, second_room.id)
        cancel_booking(booking)
        db.session.commit()

        assert booking.room_id == second_room.id
        assert booking.total_price == Decimal("160.00")
        assert [event.event_type for event in booking.events] == [
            "created",
            "room_reassigned",
            "cancelled",
        ]


def test_confirmation_and_rejection_are_separate_audited_transitions(application):
    with application.app_context():
        guest, room = create_guest_and_room()
        confirmed = create_booking(
            guest.id,
            room.id,
            date(2027, 3, 1),
            date(2027, 3, 2),
            "Pending",
        )
        db.session.commit()
        confirm_booking(confirmed)
        db.session.commit()

        rejected = create_booking(
            guest.id,
            room.id,
            date(2027, 3, 2),
            date(2027, 3, 3),
            "Pending",
        )
        db.session.commit()
        reject_booking(rejected)
        db.session.commit()

        assert confirmed.status == "Confirmed"
        assert [event.event_type for event in confirmed.events] == [
            "created",
            "confirmed",
        ]
        assert rejected.status == "Rejected"
        assert [event.event_type for event in rejected.events] == [
            "created",
            "rejected",
        ]


def test_booking_events_are_append_only(application):
    with application.app_context():
        guest, room = create_guest_and_room()
        booking = create_booking(
            guest.id,
            room.id,
            date(2026, 12, 1),
            date(2026, 12, 2),
            "Pending",
        )
        db.session.commit()

        event = booking.events[0]
        event.event_type = "modified"
        with pytest.raises(ValueError, match="append-only"):
            db.session.commit()
        db.session.rollback()


def test_payment_records_are_separate_from_booking_lifecycle(application):
    with application.app_context():
        guest, room = create_guest_and_room()
        booking = create_booking(
            guest.id,
            room.id,
            date(2027, 1, 1),
            date(2027, 1, 3),
            "Confirmed",
        )
        payment = Payment(
            booking=booking,
            amount=Decimal("50.25"),
            currency="ILS",
            status="deposit_paid",
        )
        db.session.add(payment)
        db.session.commit()

        assert booking.status == "Confirmed"
        assert booking.payments[0].amount == Decimal("50.25")
        assert not hasattr(booking, "payment_status")

        duplicate = Payment(
            booking=booking,
            amount=Decimal("1.00"),
            currency="ILS",
            status="unknown",
        )
        db.session.add(duplicate)
        with pytest.raises(IntegrityError):
            db.session.commit()
