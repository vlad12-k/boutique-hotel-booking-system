from datetime import date
from decimal import Decimal

import pytest

from hotel_app.domain import (
    BookingSource,
    ExternalReservationReference,
    Money,
    StayPeriod,
)


def test_stay_period_uses_half_open_overlap_rules():
    first = StayPeriod(date(2026, 9, 16), date(2026, 9, 18))
    adjacent = StayPeriod(date(2026, 9, 18), date(2026, 9, 20))
    overlapping = StayPeriod(date(2026, 9, 17), date(2026, 9, 19))

    assert not first.overlaps(adjacent)
    assert first.overlaps(overlapping)


def test_stay_period_rejects_empty_range():
    with pytest.raises(ValueError, match="after check-in"):
        StayPeriod(date(2026, 9, 16), date(2026, 9, 16))


def test_money_normalises_currency_without_float_arithmetic():
    value = Money(Decimal("125.50"), "ils")
    assert value.amount == Decimal("125.50")
    assert value.currency == "ILS"


def test_external_reference_requires_both_parts():
    with pytest.raises(ValueError, match="required"):
        ExternalReservationReference("booking_com", "")


def test_booking_source_contract_includes_manual_v1_sources():
    assert {
        BookingSource.PHONE,
        BookingSource.WALK_IN,
        BookingSource.BOOKING_COM,
    } <= set(BookingSource)
