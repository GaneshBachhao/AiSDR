from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SolutionSummaryDTO(BaseModel):
    """
    A generated/added Solution, as surfaced through the API.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    solution_id: UUID
    title: str
    description: str
    solution_type: str
    priority: str
    is_existing_offering: bool


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

    solutions: list[SolutionSummaryDTO] = Field(default_factory=list)

    roadmap_phases: list[str] = Field(default_factory=list)

    created_at: datetime | None = None

    updated_at: datetime | None = None
