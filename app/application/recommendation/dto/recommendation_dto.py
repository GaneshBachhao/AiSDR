from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import Field, ConfigDict


class RecommendationDTO(BaseModel):
    """
    DTO representing a Recommendation aggregate.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID

    assessment_id: UUID

    status: str

    executive_summary: str | None = None

    submitted_at: datetime | None = None

    approved_at: datetime | None = None

    solutions: list[str] = Field(default_factory=list)

    roadmap_phases: list[str] = Field(default_factory=list)

    created_at: datetime | None = None

    updated_at: datetime | None = None