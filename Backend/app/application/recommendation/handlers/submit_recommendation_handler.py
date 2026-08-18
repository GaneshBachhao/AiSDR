"""Submit Recommendation application handler."""

from __future__ import annotations

from app.application.common.exceptions.conflict_exception import ConflictException
from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.recommendation.commands.submit_recommendation import (
    SubmitRecommendationCommand,
)
from app.application.recommendation.dto.recommendation_dto import RecommendationDTO
from app.application.recommendation.mappers.recommendation_mapper import RecommendationMapper
from app.domain.recommendation.identifiers.recommendation_id import RecommendationId


class SubmitRecommendationHandler:
    """Submit a Draft Recommendation for review."""

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, command: SubmitRecommendationCommand) -> RecommendationDTO:
        async with self._unit_of_work:
            recommendation = await self._unit_of_work.recommendation_repository.get_by_id(
                RecommendationId(command.recommendation_id),
            )

            if recommendation is None:
                raise NotFoundException(
                    message="Recommendation not found.",
                    details={"recommendation_id": str(command.recommendation_id)},
                )

            try:
                recommendation.submit()
            except ValueError as exc:
                raise ConflictException(
                    message=str(exc),
                    details={"recommendation_id": str(command.recommendation_id)},
                ) from exc

            await self._unit_of_work.recommendation_repository.update(recommendation)
            await self._unit_of_work.commit()

        return RecommendationMapper.domain_to_dto(recommendation)
