from datetime import date

from models import (
    ACTIVE_BOOKING_STATUSES,
    Booking,
    Guest,
    Room,
    db,
)


NEW_BOOKING_STATUSES = frozenset({"Pending", "Confirmed"})
CANCELLATION_BLOCKED_STATUSES = frozenset({"Checked-out", "Cancelled"})
CHECK_IN_ALLOWED_STATUSES = frozenset({"Pending", "Confirmed"})


class BookingServiceError(Exception):
    """Raised when a booking operation violates a business rule."""


def create_booking(
    guest_id: int,
    room_id: int,
    check_in_date: date,
    check_out_date: date,
    booking_status: str,
) -> Booking:
    """Validate and create a new booking without committing the transaction."""

    if check_out_date <= check_in_date:
        raise BookingServiceError(
            "Check-out date must be after check-in date."
        )

    if booking_status not in NEW_BOOKING_STATUSES:
        raise BookingServiceError(
            "New bookings can only be Pending or Confirmed."
        )

    selected_guest = db.session.get(Guest, guest_id)
    selected_room = db.session.get(Room, room_id)

    if selected_guest is None or selected_room is None:
        raise BookingServiceError(
            "Please select a valid guest and room."
        )

    if selected_room.status == "Maintenance":
        raise BookingServiceError(
            "Rooms under Maintenance cannot be booked."
        )

    overlapping_booking = Booking.query.filter(
        Booking.room_id == selected_room.id,
        Booking.status.in_(ACTIVE_BOOKING_STATUSES),
        Booking.check_in_date < check_out_date,
        Booking.check_out_date > check_in_date,
    ).first()

    if overlapping_booking is not None:
        raise BookingServiceError(
            "Booking rejected: the selected room already has an "
            "active booking for overlapping dates."
        )

    total_nights = (check_out_date - check_in_date).days
    total_price = total_nights * selected_room.price_per_night

    booking = Booking(
        guest_id=selected_guest.id,
        room_id=selected_room.id,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        status=booking_status,
        total_price=total_price,
    )

    db.session.add(booking)
    return booking


def cancel_booking(booking: Booking) -> Booking:
    """Cancel an eligible booking without committing the transaction."""

    if booking.status in CANCELLATION_BLOCKED_STATUSES:
        raise BookingServiceError(
            "Booking cannot be cancelled in its current status."
        )

    booking.status = "Cancelled"
    return booking


def check_in_booking(
    booking: Booking,
    current_date: date | None = None,
) -> Booking:
    """Check in an eligible booking and mark its room as occupied."""

    if booking.status not in CHECK_IN_ALLOWED_STATUSES:
        raise BookingServiceError(
            "Only Pending or Confirmed bookings can be checked in."
        )

    effective_date = current_date or date.today()

    if effective_date < booking.check_in_date:
        raise BookingServiceError(
            "Guest cannot be checked in before the check-in date."
        )

    booking.status = "Checked-in"
    booking.room.status = "Occupied"

    return booking


def check_out_booking(booking: Booking) -> Booking:
    """Apply the booking and room status changes required for checkout."""

    if booking.status != "Checked-in":
        raise BookingServiceError(
            "Only checked-in bookings can be checked out."
        )

    booking.status = "Checked-out"
    booking.room.status = "Cleaning"

    return booking