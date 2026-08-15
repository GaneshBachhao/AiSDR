"""
Qualification request DTOs.
"""

from __future__ import annotations

from pydantic import BaseModel
from pydantic import Field


class CreateQualificationRequestDTO(BaseModel):
    """
    Request DTO to create a qualification.
    """

    lead_id: str = Field(
        ...,
        min_length=1,
    )

    assessment_id: str = Field(
        ...,
        min_length=1,
    )

    status: str | None = None

    score: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    recommendation: str | None = None


class UpdateQualificationRequestDTO(BaseModel):
    """
    Request DTO to update a qualification.
    """

    status: str | None = None

    score: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    recommendation: str | None = None