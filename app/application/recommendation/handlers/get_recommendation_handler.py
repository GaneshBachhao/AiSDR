from __future__ import annotations

from app.application.recommendation.dto.recommendation_dto import (
    RecommendationDTO,
)
from app.application.recommendation.mappers.recommendation_mapper import (
    RecommendationMapper,
)
from app.application.recommendation.queries.get_recommendation_by_id import (
    GetRecommendationByIdQuery,
)
from app.domain.recommendation.identifiers.recommendation_id import (
    RecommendationId,
)
from app.domain.recommendation.repositories.recommendation_repository import (
    RecommendationRepository,
)


class GetRecommendationHandler:
    """
    Handles retrieving a recommendation by id.
    """

    def __init__(
        self,
        repository: RecommendationRepository,
        mapper: RecommendationMapper,
    ) -> None:

        self._repository = repository
        self._mapper = mapper

    async def handle(
        self,
        query: GetRecommendationByIdQuery,
    ) -> RecommendationDTO:

        recommendation = await self._repository.get_by_id(
            RecommendationId(
                query.recommendation_id,
            ),
        )

        if recommendation is None:
            raise ValueError(
                "Recommendation not found."
            )

        return self._mapper.to_dto(
            recommendation,
        )