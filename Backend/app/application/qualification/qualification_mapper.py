"""
Qualification application mapper.
"""

from __future__ import annotations

from app.application.qualification.dto.qualification_request import (
    CreateQualificationRequestDTO,
    UpdateQualificationRequestDTO,
)
from app.application.qualification.dto.qualification_response import (
    CreateQualificationResponseDTO,
    GetQualificationResponseDTO,
    ListQualificationResponseDTO,
    UpdateQualificationResponseDTO,
)
from app.application.qualification.qualification_commands import (
    CreateQualificationCommand,
    UpdateQualificationCommand,
)
from app.domain.qualification.entities.qualification import (
    Qualification,
)


class QualificationMapper:
    """
    Maps Qualification DTOs, Commands and Domain objects.
    """

    @staticmethod
    def to_create_command(
        dto: CreateQualificationRequestDTO,
    ) -> CreateQualificationCommand:
        """
        Map request DTO to create command.
        """

        return CreateQualificationCommand(
            lead_id=dto.lead_id,
            assessment_id=dto.assessment_id,
            status=dto.status,
            score=dto.score,
            recommendation=dto.recommendation,
        )

    @staticmethod
    def to_update_command(
        qualification_id: str,
        dto: UpdateQualificationRequestDTO,
    ) -> UpdateQualificationCommand:
        """
        Map request DTO to update command.
        """

        return UpdateQualificationCommand(
            qualification_id=qualification_id,
            status=dto.status,
            score=dto.score,
            recommendation=dto.recommendation,
        )

    @staticmethod
    def to_create_response(
        qualification: Qualification,
    ) -> CreateQualificationResponseDTO:
        """
        Map Qualification aggregate to create response DTO.
        """

        return CreateQualificationResponseDTO(
            qualification_id=qualification.id.value,
            lead_id=qualification.lead_id.value,
            assessment_id=qualification.assessment_id.value,
            status=qualification.status.value,
            score=qualification.score.value,
            recommendation=qualification.recommendation,
        )

    @staticmethod
    def to_get_response(
        qualification: Qualification,
    ) -> GetQualificationResponseDTO:
        """
        Map Qualification aggregate to get response DTO.
        """

        return GetQualificationResponseDTO(
            qualification_id=qualification.id.value,
            lead_id=qualification.lead_id.value,
            assessment_id=qualification.assessment_id.value,
            status=qualification.status.value,
            score=qualification.score.value,
            recommendation=qualification.recommendation,
        )

    @staticmethod
    def to_list_response(
        qualification: Qualification,
    ) -> ListQualificationResponseDTO:
        """
        Map Qualification aggregate to list response DTO.
        """

        return ListQualificationResponseDTO(
            qualification_id=qualification.id.value,
            lead_id=qualification.lead_id.value,
            assessment_id=qualification.assessment_id.value,
            status=qualification.status.value,
            score=qualification.score.value,
        )

    @staticmethod
    def to_update_response(
        qualification: Qualification,
    ) -> UpdateQualificationResponseDTO:
        """
        Map Qualification aggregate to update response DTO.
        """

        return UpdateQualificationResponseDTO(
            qualification_id=qualification.id.value,
            lead_id=qualification.lead_id.value,
            assessment_id=qualification.assessment_id.value,
            status=qualification.status.value,
            score=qualification.score.value,
            recommendation=qualification.recommendation,
        )