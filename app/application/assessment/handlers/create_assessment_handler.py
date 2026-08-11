"""
Create Assessment handler.
"""
from __future__ import annotations

from app.application.assessment.assessment_commands import CreateAssessmentCommand
from app.application.assessment.assessment_mapper import AssessmentMapper
from app.application.assessment.assessment_validator import AssessmentValidator
from app.application.assessment.dto.assessment_response import CreateAssessmentResponseDTO
from app.application.common.handler.base_handler import BaseHandler
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.domain.assessment.entities.assessment import Assessment
from app.domain.discovery.identifiers.discovery_id import DiscoveryId


class CreateAssessmentHandler(
    BaseHandler[CreateAssessmentCommand, CreateAssessmentResponseDTO],
):
    """Handles Assessment creation."""

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, command: CreateAssessmentCommand) -> CreateAssessmentResponseDTO:
        validation = AssessmentValidator.validate_create(command)
        if validation.has_errors():
            raise ValueError(validation.error_messages())

        assessment = Assessment(
            discovery_id=DiscoveryId(command.discovery_id),
        )

        async with self._unit_of_work:
            await self._unit_of_work.assessment_repository.add(assessment)
            await self._unit_of_work.commit()

        return AssessmentMapper.to_create_response(assessment)
