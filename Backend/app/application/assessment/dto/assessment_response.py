"""
Assessment response DTOs.

Architecture Freeze v5.0
Outgoing application response contracts for the Assessment aggregate.
"""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel


class AssessmentResponseDTO(BaseModel):
    """Standard assessment response DTO."""

    assessment_id: UUID
    discovery_id: UUID
    status: str
    summary: str | None = None
    maturity_level: str
    readiness_score: float
    strengths: str | None = None
    weaknesses: str | None = None
    opportunities: str | None = None
    risks: str | None = None


class CreateAssessmentResponseDTO(AssessmentResponseDTO):
    """Response returned after creating an assessment."""


class GetAssessmentResponseDTO(AssessmentResponseDTO):
    """Response returned when retrieving an assessment."""


class UpdateAssessmentResponseDTO(AssessmentResponseDTO):
    """Response returned after updating an assessment."""


class ListAssessmentResponseDTO(AssessmentResponseDTO):
    """Response returned when listing assessments."""


class DeleteAssessmentResponseDTO(BaseModel):
    """Response returned after deleting an assessment."""

    assessment_id: UUID
    message: str
