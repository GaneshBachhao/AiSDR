from __future__ import annotations

from app.application.common.exceptions.validation_exception import (
    ValidationException,
)
from app.application.recommendation.commands.submit_recommendation import (
    SubmitRecommendationCommand,
)
from app.application.recommendation.dto.recommendation_dto import (
    RecommendationDTO,
)
from app.application.recommendation.mappers.recommendation_mapper import (
    RecommendationMapper,
)
from app.application.recommendation.validators.submit_recommendation_validator import (
    SubmitRecommendationValidator,
)
from app.domain.recommendation.identifiers.recommendation_id import (
    RecommendationId,
)
from app.domain.recommendation.repositories.recommendation_repository import (
    RecommendationRepository,
)


class SubmitRecommendationHandler:
    """
    Handles submitting a recommendation for review.
    """

    def __init__(
        self,
        repository: RecommendationRepository,
        validator: SubmitRecommendationValidator,
        mapper: RecommendationMapper,
    ) -> None:

        self._repository = repository
        self._validator = validator
        self._mapper = mapper

    async def handle(
        self,
        command: SubmitRecommendationCommand,
    ) -> RecommendationDTO:

        validation = self._validator.validate(
            command,
        )

        if not validation.is_valid:
            raise ValidationException(
                validation.errors,
            )

        recommendation = await self._repository.get_by_id(
            RecommendationId(
                command.recommendation_id,
            ),
        )

        if recommendation is None:
            raise ValueError(
                "Recommendation not found."
            )

        recommendation.submit_for_review()

        recommendation = await self._repository.save(
            recommendation,
        )

        return self._mapper.to_dto(
            recommendation,
        )