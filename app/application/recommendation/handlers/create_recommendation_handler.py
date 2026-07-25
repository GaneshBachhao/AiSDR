from __future__ import annotations

from app.application.common.exceptions.validation_exception import (
    ValidationException,
)
from app.application.recommendation.commands.create_recommendation import (
    CreateRecommendationCommand,
)
from app.application.recommendation.dto.recommendation_dto import (
    RecommendationDTO,
)
from app.application.recommendation.mappers.recommendation_mapper import (
    RecommendationMapper,
)
from app.application.recommendation.validators.create_recommendation_validator import (
    CreateRecommendationValidator,
)
from app.domain.assessment.identifiers.assessment_id import (
    AssessmentId,
)
from app.domain.recommendation.entities.recommendation import (
    Recommendation,
)
from app.domain.recommendation.repositories.recommendation_repository import (
    RecommendationRepository,
)


class CreateRecommendationHandler:
    """
    Handles creation of a Recommendation.
    """

    def __init__(
        self,
        repository: RecommendationRepository,
        validator: CreateRecommendationValidator,
        mapper: RecommendationMapper,
    ) -> None:
        self._repository = repository
        self._validator = validator
        self._mapper = mapper

    async def handle(
        self,
        command: CreateRecommendationCommand,
    ) -> RecommendationDTO:

        validation = self._validator.validate(command)

        if not validation.is_valid:
            raise ValidationException(
                validation.errors,
            )

        recommendation = Recommendation(
            assessment_id=AssessmentId(
                command.assessment_id,
            ),
        )

        recommendation.start()

        recommendation = await self._repository.save(
            recommendation,
        )

        return self._mapper.to_dto(
            recommendation,
        )