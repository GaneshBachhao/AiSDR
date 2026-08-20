"""Outcome response DTOs."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.domain.outcome.enums.outcome_type import OutcomeType


@dataclass(slots=True)
class OutcomeEventResponseDTO:
    """Standard OutcomeEvent response DTO."""

    id: str
    lead_id: str
    outcome_type: OutcomeType
    notes: str | None = None
    occurred_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
