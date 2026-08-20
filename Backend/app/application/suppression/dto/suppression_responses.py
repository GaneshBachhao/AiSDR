"""Suppression response DTOs."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.domain.suppression.enums.suppression_reason import SuppressionReason


@dataclass(slots=True)
class SuppressionEntryResponseDTO:
    """Standard SuppressionEntry response DTO."""

    id: str
    email: str
    reason: SuppressionReason
    notes: str | None = None
    suppressed_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass(slots=True)
class SuppressionCheckResponseDTO:
    """Response for GET /suppressions/check -- is this email suppressed?"""

    email: str
    suppressed: bool
    entry: SuppressionEntryResponseDTO | None = None
