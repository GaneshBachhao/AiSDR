"""Create Qualification application handler."""

from __future__ import annotations

from app.application.common.exceptions.validation_exception import ValidationException
from app.application.common.handler.base_handler import BaseHandler
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.qualification.dto.qualification_response import CreateQualificationResponseDTO
from app.application.qualification.qualification_commands import CreateQualificationCommand
from app.application.qualification.qualification_mapper import QualificationMapper
from app.application.qualification.qualification_validator import QualificationValidator
from app.domain.assessment.identifiers.assessment_id import AssessmentId
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.qualification.entities.qualification import Qualification
from app.domain.qualification.value_objects.qualification_score import QualificationScore


class CreateQualificationHandler(
    BaseHandler[CreateQualificationCommand, CreateQualificationResponseDTO],
):
    """Create a Qualification aggregate."""

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, command: CreateQualificationCommand) -> CreateQualificationResponseDTO:
        validation = QualificationValidator.validate_create(command)
        if validation.has_errors():
            raise ValidationException(
                message="Qualification validation failed.",
                details={error.field: error.message for error in validation.errors},
            )

        qualification = Qualification(
            lead_id=LeadId(command.lead_id),
            assessment_id=AssessmentId(command.assessment_id),
        )

        if command.status is not None:
            status = QualificationValidator.normalize_status(command.status)
            if status is not None:
                qualification.update_status(status)

        if command.score is not None:
            qualification.update_score(
                QualificationScore(command.score),
            )

        if command.recommendation is not None:
            qualification.update_recommendation(command.recommendation)

        async with self._unit_of_work:
            await self._unit_of_work.qualification_repository.add(qualification)
            await self._unit_of_work.commit()

        return QualificationMapper.to_create_response(qualification)
