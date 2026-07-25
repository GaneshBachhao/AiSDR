from __future__ import annotations

from app.application.assessment.commands.start_assessment import (
    StartAssessmentCommand,
)
from app.application.assessment.dto.assessment_dto import (
    AssessmentDTO,
)
from app.application.assessment.mappers.assessment_mapper import (
    AssessmentMapper,
)
from app.application.assessment.validators.start_assessment_validator import (
    StartAssessmentValidator,
)
from app.application.common.exceptions.validation_exception import (
    ValidationException,
)
from app.domain.assessment.entities.assessment import (
    Assessment,
)
from app.domain.assessment.repositories.assessment_repository import (
    AssessmentRepository,
)
from app.domain.assessment.services.assessment_service import (
    AssessmentService,
)
from app.domain.discovery.identifiers.discovery_session_id import (
    DiscoverySessionId,
)


class StartAssessmentHandler:
    """
    Handles StartAssessmentCommand.
    """

    def __init__(
        self,
        repository: AssessmentRepository,
        validator: StartAssessmentValidator,
        mapper: AssessmentMapper,
    ) -> None:
        self._repository = repository
        self._validator = validator
        self._mapper = mapper

    async def handle(
        self,
        command: StartAssessmentCommand,
    ) -> AssessmentDTO:
        """
        Start a new assessment.
        """

        validation = self._validator.validate(
            command,
        )

        if not validation.is_valid:
            raise ValidationException(
                validation.errors,
            )

        discovery_session_id = DiscoverySessionId(
            command.discovery_session_id,
        )

        existing = await self._repository.get_by_discovery(
            discovery_session_id,
        )

        if existing is not None:
            return self._mapper.to_dto(
                existing,
            )

        assessment = Assessment(
            discovery_session_id=discovery_session_id,
        )

        AssessmentService.start(
            assessment,
        )

        if command.summary:
            assessment.summary = command.summary

        assessment = await self._repository.save(
            assessment,
        )

        return self._mapper.to_dto(
            assessment,
        )