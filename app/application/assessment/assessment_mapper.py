"""
Assessment application mapper.

Maps request DTOs -> commands and domain entities -> response DTOs.
"""
from __future__ import annotations

from app.application.assessment.assessment_commands import (
    CreateAssessmentCommand,
    UpdateAssessmentCommand,
)
from app.application.assessment.dto.assessment_request import (
    CreateAssessmentRequestDTO,
    UpdateAssessmentRequestDTO,
)
from app.application.assessment.dto.assessment_response import (
    CreateAssessmentResponseDTO,
    GetAssessmentResponseDTO,
    ListAssessmentResponseDTO,
    UpdateAssessmentResponseDTO,
)
from app.domain.assessment.entities.assessment import Assessment


class AssessmentMapper:
    """Maps Assessment application/domain objects."""

    @staticmethod
    def to_create_command(dto: CreateAssessmentRequestDTO) -> CreateAssessmentCommand:
        return CreateAssessmentCommand(discovery_id=dto.discovery_id)

    @staticmethod
    def to_update_command(
        assessment_id: str,
        dto: UpdateAssessmentRequestDTO,
    ) -> UpdateAssessmentCommand:
        return UpdateAssessmentCommand(
            assessment_id=assessment_id,
            summary=dto.summary,
            maturity_level=dto.maturity_level,
            readiness_score=dto.readiness_score,
            strengths=dto.strengths,
            weaknesses=dto.weaknesses,
            opportunities=dto.opportunities,
            risks=dto.risks,
        )

    @staticmethod
    def _maturity_value(assessment: Assessment) -> str:
        maturity = assessment.maturity_level
        value = getattr(maturity, "value", None)
        if value is not None:
            return str(value)
        return str(getattr(maturity, "name", maturity))

    @staticmethod
    def _status_value(assessment: Assessment) -> str:
        status = getattr(assessment, "status", None)
        if status is None:
            return "Created"
        value = getattr(status, "value", None)
        if value is not None:
            return str(value)
        return str(getattr(status, "name", status))

    @staticmethod
    def _response_kwargs(assessment: Assessment) -> dict:
        return {
            "assessment_id": assessment.id.value,
            "discovery_id": assessment.discovery_id.value,
            "status": AssessmentMapper._status_value(assessment),
            "summary": assessment.summary,
            "maturity_level": AssessmentMapper._maturity_value(assessment),
            "readiness_score": assessment.score.overall_score,
            "strengths": getattr(assessment, "strengths", None),
            "weaknesses": getattr(assessment, "weaknesses", None),
            "opportunities": getattr(
                assessment,
                "opportunities_summary",
                getattr(assessment, "opportunities", None),
            ),
            "risks": getattr(assessment, "risks", None),
        }

    @staticmethod
    def to_create_response(assessment: Assessment) -> CreateAssessmentResponseDTO:
        return CreateAssessmentResponseDTO(**AssessmentMapper._response_kwargs(assessment))

    @staticmethod
    def to_get_response(assessment: Assessment) -> GetAssessmentResponseDTO:
        return GetAssessmentResponseDTO(**AssessmentMapper._response_kwargs(assessment))

    @staticmethod
    def to_list_response(assessment: Assessment) -> ListAssessmentResponseDTO:
        return ListAssessmentResponseDTO(**AssessmentMapper._response_kwargs(assessment))

    @staticmethod
    def to_update_response(assessment: Assessment) -> UpdateAssessmentResponseDTO:
        return UpdateAssessmentResponseDTO(**AssessmentMapper._response_kwargs(assessment))
