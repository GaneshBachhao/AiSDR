"""Outcome request DTOs."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.domain.outcome.enums.outcome_type import OutcomeType


@dataclass(slots=True)
class CreateOutcomeEventRequestDTO:
    """Request to record an outcome for a Lead."""

    lead_id: str
    outcome_type: OutcomeType
    occurred_at: datetime | None = None
    notes: str | None = None
