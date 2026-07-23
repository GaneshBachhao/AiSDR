# app/application/assessment/handlers/generate_assessment_handler.py

"""
Generate Assessment Handler.
"""

from __future__ import annotations

from app.application.assessment.commands.generate_assessment import (
    GenerateAssessmentCommand,
)
from app.application.assessment.dto.assessment_dto import (
    AssessmentDTO,
)
from app.application.assessment.mappers.assessment_mapper import (
    AssessmentMapper,
)
from app.application.assessment.validators.generate_assessment_validator import (
    GenerateAssessmentValidator,
)
from app.application.common.handler.base_handler import (
    BaseHandler,
)
from app.application.common.handler.handler_context import (
    HandlerContext,
)
from app.application.common.handler.handler_result import (
    HandlerResult,
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


class GenerateAssessmentHandler(
    BaseHandler[
        GenerateAssessmentCommand,
        AssessmentDTO,
    ]
):
    """
    Application handler responsible for generating
    an assessment for a discovery session.
    """

    def __init__(
        self,
        repository: AssessmentRepository,
        service: AssessmentService | None = None,
        validator: GenerateAssessmentValidator | None = None,
    ) -> None:
        self._repository = repository
        self._service = service or AssessmentService()
        self._validator = (
            validator
            if validator is not None
            else GenerateAssessmentValidator()
        )

    async def handle(
        self,
        request: GenerateAssessmentCommand,
        context: HandlerContext,
    ) -> HandlerResult[AssessmentDTO]:
        """
        Generate an assessment.
        """

        validation = self._validator.validate(
            request,
        )

        if validation.has_errors:
            return HandlerResult.failure(
                message="Assessment validation failed.",
                errors=validation.errors,
            )

        discovery_session_id = DiscoverySessionId(
            request.discovery_session_id,
        )

        assessment = await self._repository.get_by_discovery(
            discovery_session_id,
        )

        if assessment is None:

            assessment = Assessment(
                discovery_session_id=discovery_session_id,
            )

            self._service.start(
                assessment,
            )

            assessment = await self._repository.save(
                assessment,
            )

        dto = AssessmentMapper.to_dto(
            assessment,
        )

        return HandlerResult.ok(
            data=dto,
            message="Assessment generated successfully.",
        )