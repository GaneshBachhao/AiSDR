from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class RecommendationDTO:
    """
    Data transfer object representing a recommendation.
    """

    id: UUID

    assessment_id: UUID

    status: str

    created_at: datetime

    submitted_at: datetime | None

    approved_at: datetime | None