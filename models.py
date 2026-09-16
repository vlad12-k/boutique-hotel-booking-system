"""Compatibility imports for the original academic module path."""

from hotel_app.models import (  # noqa: F401
    ACTIVE_BOOKING_STATUSES,
    BOOKING_STATUSES,
    ROOM_STATUSES,
    STAFF_ROLES,
    Booking,
    Guest,
    NotificationLog,
    Room,
    SecurityAuditEvent,
    StaffAccount,
    db,
)


__all__ = [
    "ACTIVE_BOOKING_STATUSES",
    "BOOKING_STATUSES",
    "ROOM_STATUSES",
    "STAFF_ROLES",
    "Booking",
    "Guest",
    "NotificationLog",
    "Room",
    "SecurityAuditEvent",
    "StaffAccount",
    "db",
]
