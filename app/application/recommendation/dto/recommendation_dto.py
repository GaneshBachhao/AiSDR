"""
Recommendation DTO models.
"""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SolutionDTO(BaseModel):
    """
    Application representation of a proposed solution.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    title: str

    description: str

    solution_type: str

    priority: str


class RoadmapPhaseDTO(BaseModel):
    """
    Application representation of an implementation phase.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str

    description: str

    order: int


class RecommendationDTO(BaseModel):
    """
    Application representation of a Recommendation.

    This DTO is independent of API contracts.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: UUID

    assessment_id: UUID

    status: str

    executive_summary: str | None = None

    solutions: list[SolutionDTO]

    roadmap_phases: list[RoadmapPhaseDTO]