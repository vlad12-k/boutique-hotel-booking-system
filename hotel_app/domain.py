from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import StrEnum


class BookingSource(StrEnum):
    DIRECT = "direct"
    PHONE = "phone"
    WALK_IN = "walk_in"
    BOOKING_COM = "booking_com"
    OTHER = "other"


class BookingLifecycle(StrEnum):
    REQUESTED = "requested"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"


class PaymentStatus(StrEnum):
    UNPAID = "unpaid"
    DEPOSIT_DUE = "deposit_due"
    DEPOSIT_PAID = "deposit_paid"
    PAID_IN_FULL = "paid_in_full"
    REFUNDED = "refunded"


class RoomOperationalState(StrEnum):
    READY = "ready"
    CLEANING = "cleaning"
    MAINTENANCE = "maintenance"


@dataclass(frozen=True, slots=True)
class StayPeriod:
    """Half-open hotel stay period: check-in is included, check-out is excluded."""

    check_in: date
    check_out: date

    def __post_init__(self) -> None:
        if self.check_out <= self.check_in:
            raise ValueError("Check-out date must be after check-in date.")

    def overlaps(self, other: "StayPeriod") -> bool:
        return self.check_in < other.check_out and self.check_out > other.check_in


@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("Money amount cannot be negative.")
        if len(self.currency) != 3 or not self.currency.isalpha():
            raise ValueError("Currency must be a three-letter ISO code.")
        object.__setattr__(self, "currency", self.currency.upper())


@dataclass(frozen=True, slots=True)
class ExternalReservationReference:
    provider: str
    reference: str

    def __post_init__(self) -> None:
        if not self.provider.strip() or not self.reference.strip():
            raise ValueError("Provider and external reference are required.")
