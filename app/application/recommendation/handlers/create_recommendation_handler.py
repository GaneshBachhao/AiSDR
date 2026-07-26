from __future__ import annotations

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
from app.application.contracts.repositories.recommendation_repository import (
    RecommendationRepository,
)
from app.domain.assessment.identifiers.assessment_id import (
    AssessmentId,
)
from app.domain.recommendation.entities.recommendation import (
    Recommendation,
)


class CreateRecommendationHandler:
    """
    Handles creation of Recommendation aggregates.
    """

    def __init__(
        self,
        repository: RecommendationRepository,
        validator: CreateRecommendationValidator,
        mapper: RecommendationMapper,
    ):
        self._repository = repository
        self._validator = validator
        self._mapper = mapper

    async def handle(
        self,
        command: CreateRecommendationCommand,
    ) -> RecommendationDTO:

        validation = self._validator.validate(
            command,
        )

        if not validation.success:
            raise ValueError(
                validation.errors,
            )

        recommendation = Recommendation(
            assessment_id=AssessmentId(
                command.assessment_id,
            ),
        )

        await self._repository.save(
            recommendation,
        )

        return self._mapper.domain_to_dto(
            recommendation,
        )