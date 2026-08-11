"""Get Recommendation application handler."""

from __future__ import annotations

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.recommendation.dto.recommendation_dto import RecommendationDTO
from app.application.recommendation.mappers.recommendation_mapper import RecommendationMapper
from app.application.recommendation.queries.get_recommendation_by_id import GetRecommendationByIdQuery
from app.domain.recommendation.identifiers.recommendation_id import RecommendationId


class GetRecommendationHandler:
    """Retrieve a Recommendation by id."""

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, query: GetRecommendationByIdQuery) -> RecommendationDTO:
        async with self._unit_of_work:
            recommendation = await self._unit_of_work.recommendation_repository.get_by_id(
                RecommendationId(query.recommendation_id),
            )

        if recommendation is None:
            raise NotFoundException(
                message="Recommendation not found.",
                details={"recommendation_id": str(query.recommendation_id)},
            )

        return RecommendationMapper.domain_to_dto(recommendation)
