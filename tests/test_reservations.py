from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from app.main import ReservationStatus, app, can_transition, overlaps, public_app_config


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


def test_landing_page_is_available() -> None:
    response = TestClient(app).get("/")
    assert response.status_code == 200
    assert "GestionLab" in response.text
    assert "Continuar con Google" in response.text


def test_public_config_does_not_enable_placeholder_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SUPABASE_URL", "https://your-project.supabase.co")
    monkeypatch.setenv("SUPABASE_ANON_KEY", "replace-me")
    assert not public_app_config().auth_enabled
