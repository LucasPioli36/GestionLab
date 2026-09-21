from datetime import datetime

import pytest

from app.main import ReservationStatus, can_transition, overlaps


def test_active_reservations_overlap_when_intervals_cross() -> None:
    assert overlaps(datetime(2026, 9, 22, 10), datetime(2026, 9, 22, 11), datetime(2026, 9, 22, 10, 30), datetime(2026, 9, 22, 11, 30))


def test_back_to_back_reservations_do_not_overlap() -> None:
    assert not overlaps(datetime(2026, 9, 22, 10), datetime(2026, 9, 22, 11), datetime(2026, 9, 22, 11), datetime(2026, 9, 22, 12))


def test_reservation_requires_a_valid_interval() -> None:
    with pytest.raises(ValueError):
        overlaps(datetime(2026, 9, 22, 11), datetime(2026, 9, 22, 10), datetime(2026, 9, 22, 12), datetime(2026, 9, 22, 13))


def test_pending_reservation_can_be_confirmed() -> None:
    assert can_transition(ReservationStatus.PENDING, ReservationStatus.CONFIRMED)


def test_final_reservation_cannot_change_status() -> None:
    assert not can_transition(ReservationStatus.COMPLETED, ReservationStatus.CANCELLED)
