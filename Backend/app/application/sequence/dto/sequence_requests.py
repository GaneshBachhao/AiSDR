"""Sequence request DTOs."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.sequence.enums.touch_channel import TouchChannel


@dataclass(slots=True)
class TouchInputDTO:
    """One planned touch, as supplied when creating a Sequence."""

    channel: TouchChannel
    wait_days: int


@dataclass(slots=True)
class CreateSequenceRequestDTO:
    """Request to create a Sequence for a Lead."""

    lead_id: str
    touches: list[TouchInputDTO]
