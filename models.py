"""Compatibility imports for the original academic module path."""

from hotel_app.models import (  # noqa: F401
    ACTIVE_BOOKING_STATUSES,
    BOOKING_EVENT_TYPES,
    BOOKING_SOURCES,
    BOOKING_STATUSES,
    PAYMENT_STATUSES,
    ROOM_OPERATIONAL_STATES,
    ROOM_STATUSES,
    STAFF_ROLES,
    Booking,
    BookingEvent,
    Guest,
    NotificationLog,
    Payment,
    Room,
    RoomType,
    SecurityAuditEvent,
    StaffAccount,
    db,
)


__all__ = [
    "ACTIVE_BOOKING_STATUSES",
    "BOOKING_EVENT_TYPES",
    "BOOKING_SOURCES",
    "BOOKING_STATUSES",
    "PAYMENT_STATUSES",
    "ROOM_OPERATIONAL_STATES",
    "ROOM_STATUSES",
    "STAFF_ROLES",
    "Booking",
    "BookingEvent",
    "Guest",
    "NotificationLog",
    "Payment",
    "Room",
    "RoomType",
    "SecurityAuditEvent",
    "StaffAccount",
    "db",
]
