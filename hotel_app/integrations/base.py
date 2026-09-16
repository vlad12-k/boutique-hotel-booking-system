from dataclasses import dataclass
from typing import Any, Mapping, Protocol

from hotel_app.domain import BookingSource, ExternalReservationReference, StayPeriod


@dataclass(frozen=True, slots=True)
class InboundReservation:
    source: BookingSource
    stay: StayPeriod
    guest_display_name: str
    external_reference: ExternalReservationReference | None = None
    requested_room_type: str | None = None


class ReservationAdapter(Protocol):
    """Boundary for future manual imports, channel managers and other providers."""

    def normalise(self, payload: Mapping[str, Any]) -> InboundReservation:
        """Convert a provider payload into the internal reservation contract."""
