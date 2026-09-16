from datetime import date
from decimal import Decimal

from sqlalchemy.exc import DBAPIError

from hotel_app.domain import BookingSource, RoomOperationalState
from hotel_app.models import (
    ACTIVE_BOOKING_STATUSES,
    BOOKING_SOURCES,
    Booking,
    BookingEvent,
    Guest,
    Room,
    db,
)


NEW_BOOKING_STATUSES = frozenset({"Pending", "Confirmed"})
CANCELLATION_BLOCKED_STATUSES = frozenset(
    {"Rejected", "Checked-out", "Cancelled"}
)
CHECK_IN_ALLOWED_STATUSES = frozenset({"Pending", "Confirmed"})
AVAILABILITY_CONFLICT_SQLSTATES = frozenset({"23P01", "40001", "40P01"})
EXTERNAL_REFERENCE_CONSTRAINT = "uq_booking_external_reference"


class BookingServiceError(Exception):
    """Raised when a booking operation violates a business rule."""


def is_availability_conflict(error: DBAPIError) -> bool:
    """Return whether PostgreSQL rejected a concurrent availability write."""
    return getattr(error.orig, "sqlstate", None) in AVAILABILITY_CONFLICT_SQLSTATES


def is_external_reference_conflict(error: DBAPIError) -> bool:
    """Return whether PostgreSQL rejected a duplicate provider reference."""
    diagnostic = getattr(error.orig, "diag", None)
    return (
        getattr(error.orig, "sqlstate", None) == "23505"
        and getattr(diagnostic, "constraint_name", None)
        == EXTERNAL_REFERENCE_CONSTRAINT
    )


def _assert_room_available(
    room: Room,
    check_in_date: date,
    check_out_date: date,
    *,
    exclude_booking_id: int | None = None,
) -> None:
    if room.operational_state == RoomOperationalState.MAINTENANCE.value:
        raise BookingServiceError("Rooms under Maintenance cannot be booked.")

    overlapping_query = Booking.query.filter(
        Booking.room_id == room.id,
        Booking.status.in_(ACTIVE_BOOKING_STATUSES),
        Booking.check_in_date < check_out_date,
        Booking.check_out_date > check_in_date,
    )
    if exclude_booking_id is not None:
        overlapping_query = overlapping_query.filter(Booking.id != exclude_booking_id)

    if overlapping_query.first() is not None:
        raise BookingServiceError(
            "Booking rejected: the selected room already has an "
            "active booking for overlapping dates."
        )


def _append_event(
    booking: Booking,
    event_type: str,
    *,
    actor_staff_account_id: int | None = None,
    from_status: str | None = None,
    to_status: str | None = None,
    from_room_id: int | None = None,
    to_room_id: int | None = None,
) -> BookingEvent:
    event = BookingEvent(
        event_type=event_type,
        actor_staff_account_id=actor_staff_account_id,
        from_status=from_status,
        to_status=to_status,
        from_room_id=from_room_id,
        to_room_id=to_room_id,
    )
    booking.events.append(event)
    return event


def create_booking(
    guest_id: int,
    room_id: int,
    check_in_date: date,
    check_out_date: date,
    booking_status: str,
    *,
    source: str = BookingSource.DIRECT.value,
    external_provider: str | None = None,
    external_reference: str | None = None,
    actor_staff_account_id: int | None = None,
) -> Booking:
    """Validate and create a booking and its initial history events."""
    if check_out_date <= check_in_date:
        raise BookingServiceError("Check-out date must be after check-in date.")
    if booking_status not in NEW_BOOKING_STATUSES:
        raise BookingServiceError("New bookings can only be Pending or Confirmed.")
    if source not in BOOKING_SOURCES:
        raise BookingServiceError("Please select a valid booking source.")

    provider = external_provider.strip() if external_provider else None
    reference = external_reference.strip() if external_reference else None
    if bool(provider) != bool(reference):
        raise BookingServiceError(
            "External provider and reservation reference must be supplied together."
        )
    if provider and Booking.query.filter_by(
        external_provider=provider, external_reference=reference
    ).first():
        raise BookingServiceError("This external reservation is already recorded.")

    selected_guest = db.session.get(Guest, guest_id)
    selected_room = db.session.get(Room, room_id)
    if selected_guest is None or selected_room is None:
        raise BookingServiceError("Please select a valid guest and room.")

    _assert_room_available(selected_room, check_in_date, check_out_date)

    total_nights = (check_out_date - check_in_date).days
    total_price = (Decimal(total_nights) * selected_room.price_per_night).quantize(
        Decimal("0.01")
    )
    booking = Booking(
        guest_id=selected_guest.id,
        room_id=selected_room.id,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        status=booking_status,
        source=source,
        external_provider=provider,
        external_reference=reference,
        total_price=total_price,
        currency=selected_room.currency,
    )
    _append_event(
        booking,
        "created",
        actor_staff_account_id=actor_staff_account_id,
        to_status=booking_status,
        to_room_id=selected_room.id,
    )
    if booking_status == "Confirmed":
        _append_event(
            booking,
            "confirmed",
            actor_staff_account_id=actor_staff_account_id,
            to_status="Confirmed",
        )

    db.session.add(booking)
    return booking


def confirm_booking(
    booking: Booking, *, actor_staff_account_id: int | None = None
) -> Booking:
    if booking.status != "Pending":
        raise BookingServiceError("Only pending bookings can be confirmed.")
    _assert_room_available(
        booking.room,
        booking.check_in_date,
        booking.check_out_date,
        exclude_booking_id=booking.id,
    )
    booking.status = "Confirmed"
    _append_event(
        booking,
        "confirmed",
        actor_staff_account_id=actor_staff_account_id,
        from_status="Pending",
        to_status="Confirmed",
    )
    return booking


def reject_booking(
    booking: Booking, *, actor_staff_account_id: int | None = None
) -> Booking:
    if booking.status != "Pending":
        raise BookingServiceError("Only pending bookings can be rejected.")
    booking.status = "Rejected"
    _append_event(
        booking,
        "rejected",
        actor_staff_account_id=actor_staff_account_id,
        from_status="Pending",
        to_status="Rejected",
    )
    return booking


def record_booking_modified(
    booking: Booking, *, actor_staff_account_id: int | None = None
) -> Booking:
    """Record an audited modification performed by a future edit workflow."""
    _append_event(
        booking,
        "modified",
        actor_staff_account_id=actor_staff_account_id,
        from_status=booking.status,
        to_status=booking.status,
    )
    return booking


def reassign_booking_room(
    booking: Booking,
    room_id: int,
    *,
    actor_staff_account_id: int | None = None,
) -> Booking:
    if booking.status not in ACTIVE_BOOKING_STATUSES:
        raise BookingServiceError("Only active bookings can be reassigned.")
    new_room = db.session.get(Room, room_id)
    if new_room is None:
        raise BookingServiceError("Please select a valid room.")
    if new_room.id == booking.room_id:
        raise BookingServiceError("The booking is already assigned to this room.")

    _assert_room_available(new_room, booking.check_in_date, booking.check_out_date)
    previous_room_id = booking.room_id
    booking.room = new_room
    booking.total_price = (
        Decimal((booking.check_out_date - booking.check_in_date).days)
        * new_room.price_per_night
    ).quantize(Decimal("0.01"))
    booking.currency = new_room.currency
    _append_event(
        booking,
        "room_reassigned",
        actor_staff_account_id=actor_staff_account_id,
        from_room_id=previous_room_id,
        to_room_id=new_room.id,
    )
    return booking


def cancel_booking(
    booking: Booking, *, actor_staff_account_id: int | None = None
) -> Booking:
    if booking.status in CANCELLATION_BLOCKED_STATUSES:
        raise BookingServiceError("Booking cannot be cancelled in its current status.")
    previous_status = booking.status
    booking.status = "Cancelled"
    _append_event(
        booking,
        "cancelled",
        actor_staff_account_id=actor_staff_account_id,
        from_status=previous_status,
        to_status="Cancelled",
    )
    return booking


def check_in_booking(
    booking: Booking,
    current_date: date | None = None,
    *,
    actor_staff_account_id: int | None = None,
) -> Booking:
    """Check in a booking; room occupancy is derived from this state."""
    if booking.status not in CHECK_IN_ALLOWED_STATUSES:
        raise BookingServiceError(
            "Only Pending or Confirmed bookings can be checked in."
        )
    effective_date = current_date or date.today()
    if effective_date < booking.check_in_date:
        raise BookingServiceError("Guest cannot be checked in before the check-in date.")

    previous_status = booking.status
    booking.status = "Checked-in"
    _append_event(
        booking,
        "checked_in",
        actor_staff_account_id=actor_staff_account_id,
        from_status=previous_status,
        to_status="Checked-in",
    )
    return booking


def check_out_booking(
    booking: Booking, *, actor_staff_account_id: int | None = None
) -> Booking:
    if booking.status != "Checked-in":
        raise BookingServiceError("Only checked-in bookings can be checked out.")

    booking.status = "Checked-out"
    booking.room.operational_state = RoomOperationalState.CLEANING.value
    _append_event(
        booking,
        "checked_out",
        actor_staff_account_id=actor_staff_account_id,
        from_status="Checked-in",
        to_status="Checked-out",
    )
    return booking
