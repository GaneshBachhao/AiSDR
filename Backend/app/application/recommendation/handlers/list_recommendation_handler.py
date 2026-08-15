"""List Recommendation application handler."""

from __future__ import annotations

from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.recommendation.dto.recommendation_dto import RecommendationDTO
from app.application.recommendation.mappers.recommendation_mapper import RecommendationMapper
from app.application.recommendation.queries.list_recommendations import ListRecommendationsQuery

class ListRecommendationHandler:
    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, query: ListRecommendationsQuery) -> list[RecommendationDTO]:
        async with self._unit_of_work:
            recommendations = await self._unit_of_work.recommendation_repository.list(
                page=query.page, page_size=query.page_size,
            )
        return [RecommendationMapper.domain_to_dto(item) for item in recommendations]
