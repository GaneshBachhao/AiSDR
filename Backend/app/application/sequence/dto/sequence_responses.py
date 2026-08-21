"""Sequence response DTOs."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.domain.sequence.enums.sequence_status import SequenceStatus
from app.domain.sequence.enums.touch_channel import TouchChannel


@dataclass(slots=True)
class TouchResponseDTO:
    """One planned touch, as returned to a caller."""

    channel: TouchChannel
    wait_days: int
    content: str | None = None


@dataclass(slots=True)
class SequenceResponseDTO:
    """Standard Sequence response DTO."""

    id: str
    lead_id: str
    touches: list[TouchResponseDTO]
    status: SequenceStatus
    current_touch_index: int
    started_at: datetime | None = None
    ended_at: datetime | None = None
    stop_reason: str | None = None
    next_touch_due_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
