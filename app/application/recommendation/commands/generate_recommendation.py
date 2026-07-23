"""
Generate Recommendation Command

Represents a request to generate AI recommendations
from an Assessment.
"""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class GenerateRecommendationCommand(BaseModel):
    """
    Command used by GenerateRecommendationHandler.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        str_strip_whitespace=True,
    )

    assessment_id: UUID = Field(
        ...,
        description="Assessment identifier",
    )

    include_roadmap: bool = Field(
        default=True,
        description="Include implementation roadmap",
    )

    include_roi: bool = Field(
        default=True,
        description="Include ROI estimation",
    )

    include_risks: bool = Field(
        default=True,
        description="Include implementation risks",
    )