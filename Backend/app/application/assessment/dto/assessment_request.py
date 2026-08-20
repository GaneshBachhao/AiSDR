"""
Assessment request DTOs.

Architecture Freeze v5.0
Application-facing request contracts for the Assessment aggregate.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class CreateAssessmentRequestDTO(BaseModel):
    """Request DTO to create an assessment."""

    discovery_id: str = Field(..., min_length=1)


class CompleteAssessmentRequestDTO(BaseModel):
    """Request DTO to complete an assessment."""

    summary: str | None = None


class UpdateAssessmentRequestDTO(BaseModel):
    """Request DTO to update an assessment."""

    summary: str | None = None
    maturity_level: str | None = None
    readiness_score: float | None = Field(default=None, ge=0, le=100)
    strengths: str | None = None
    weaknesses: str | None = None
    opportunities: str | None = None
    risks: str | None = None
