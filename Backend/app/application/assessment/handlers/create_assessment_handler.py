"""
Create Assessment handler.
"""

from __future__ import annotations

from sqlalchemy.exc import IntegrityError

from app.application.assessment.assessment_commands import CreateAssessmentCommand
from app.application.assessment.assessment_mapper import AssessmentMapper
from app.application.assessment.assessment_validator import AssessmentValidator
from app.application.assessment.dto.assessment_response import CreateAssessmentResponseDTO
from app.application.common.exceptions.conflict_exception import ConflictException
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

        discovery_id = DiscoveryId(command.discovery_id)

        assessment = Assessment(
            discovery_id=discovery_id,
        )

        # A Discovery can have at most one Assessment (discovery_id is a
        # unique column, app/infrastructure/persistence/models/assessment_model.py).
        # This pre-check gives a clean 409 for the common case; the
        # IntegrityError fallback below covers the race-condition case
        # where two requests for the same discovery_id land concurrently
        # (mirrors CreateDiscoveryHandler's own one-per-Lead check).
        try:
            async with self._unit_of_work:
                existing = await self._unit_of_work.assessment_repository.get_by_discovery(discovery_id)
                if existing is not None:
                    raise ConflictException(
                        message="Assessment already exists for this discovery.",
                        details={"discovery_id": command.discovery_id},
                    )

                await self._unit_of_work.assessment_repository.add(assessment)
                await self._unit_of_work.commit()
        except IntegrityError as exc:
            raise ConflictException(
                message="Assessment already exists for this discovery.",
                details={"discovery_id": command.discovery_id},
            ) from exc

        return AssessmentMapper.to_create_response(assessment)
