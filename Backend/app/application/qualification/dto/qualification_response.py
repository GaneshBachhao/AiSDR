"""
Qualification response DTOs.
"""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel


class QualificationResponseDTO(BaseModel):
    """
    Standard qualification response DTO.
    """

    qualification_id: UUID

    lead_id: UUID

    assessment_id: UUID

    status: str

    score: float

    recommendation: str | None


class CreateQualificationResponseDTO(
    QualificationResponseDTO,
):
    """
    Response DTO returned after creating a qualification.
    """


class GetQualificationResponseDTO(
    QualificationResponseDTO,
):
    """
    Response DTO returned when retrieving a qualification.
    """


class UpdateQualificationResponseDTO(
    QualificationResponseDTO,
):
    """
    Response DTO returned after updating a qualification.
    """


class ListQualificationResponseDTO(
    BaseModel,
):
    """
    Response DTO returned when listing qualifications.
    """

    qualification_id: UUID

    lead_id: UUID

    assessment_id: UUID

    status: str

    score: float


class DeleteQualificationResponseDTO(
    BaseModel,
):
    """
    Response DTO returned after deleting a qualification.
    """

    qualification_id: UUID

    message: str
