from __future__ import annotations

from app.application.assessment.commands.update_assessment_score import (
    UpdateAssessmentScoreCommand,
)
from app.application.assessment.dto.assessment_dto import (
    AssessmentDTO,
)
from app.application.assessment.mappers.assessment_mapper import (
    AssessmentMapper,
)
from app.application.assessment.validators.update_assessment_score_validator import (
    UpdateAssessmentScoreValidator,
)
from app.application.common.exceptions.validation_exception import (
    ValidationException,
)
from app.domain.assessment.identifiers.assessment_id import (
    AssessmentId,
)
from app.domain.assessment.repositories.assessment_repository import (
    AssessmentRepository,
)
from app.domain.assessment.services.assessment_service import (
    AssessmentService,
)
from app.domain.assessment.value_objects.assessment_score import (
    AssessmentScore,
)


class UpdateAssessmentScoreHandler:
    """
    Handles UpdateAssessmentScoreCommand.
    """

    def __init__(
        self,
        repository: AssessmentRepository,
        validator: UpdateAssessmentScoreValidator,
        mapper: AssessmentMapper,
    ) -> None:
        self._repository = repository
        self._validator = validator
        self._mapper = mapper

    async def handle(
        self,
        command: UpdateAssessmentScoreCommand,
    ) -> AssessmentDTO:
        """
        Update an assessment score and maturity level.
        """

        validation = self._validator.validate(
            command,
        )

        if not validation.is_valid:
            raise ValidationException(
                validation.errors,
            )

        assessment = await self._repository.get_by_id(
            AssessmentId(
                command.assessment_id,
            ),
        )

        if assessment is None:
            raise ValueError(
                "Assessment not found."
            )

        score = AssessmentScore(
            overall_score=command.overall_score,
        )

        AssessmentService.update_score(
            assessment,
            score,
        )

        maturity = AssessmentService.determine_maturity(
            score,
        )

        AssessmentService.update_maturity(
            assessment,
            maturity,
        )

        assessment = await self._repository.save(
            assessment,
        )

        return self._mapper.to_dto(
            assessment,
        )