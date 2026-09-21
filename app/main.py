from datetime import datetime
from enum import StrEnum

from fastapi import FastAPI
from pydantic import BaseModel


class ReservationStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"
    EXPIRED = "expired"


ALLOWED_TRANSITIONS = {
    ReservationStatus.PENDING: {ReservationStatus.CONFIRMED, ReservationStatus.CANCELLED, ReservationStatus.EXPIRED},
    ReservationStatus.CONFIRMED: {ReservationStatus.CANCELLED, ReservationStatus.COMPLETED, ReservationStatus.NO_SHOW},
    ReservationStatus.CANCELLED: set(),
    ReservationStatus.COMPLETED: set(),
    ReservationStatus.NO_SHOW: set(),
    ReservationStatus.EXPIRED: set(),
}


def can_transition(current: ReservationStatus, target: ReservationStatus) -> bool:
    return target in ALLOWED_TRANSITIONS[current]


def overlaps(starts_at: datetime, ends_at: datetime, other_starts_at: datetime, other_ends_at: datetime) -> bool:
    if starts_at >= ends_at or other_starts_at >= other_ends_at:
        raise ValueError("La hora de finalización debe ser posterior a la de inicio.")
    return starts_at < other_ends_at and other_starts_at < ends_at


class HealthResponse(BaseModel):
    status: str
    service: str


app = FastAPI(title="Agenda MVP", version="0.1.0")


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="agenda-mvp")


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    return {"message": "Agenda MVP base lista. Ver docs/day-1-scope.md."}
