"""Create Recommendation application handler."""

from __future__ import annotations

from app.application.recommendation.commands.create_recommendation import CreateRecommendationCommand
from app.application.recommendation.dto.recommendation_dto import RecommendationDTO
from app.application.recommendation.mappers.recommendation_mapper import RecommendationMapper
from app.application.recommendation.validators.create_recommendation_validator import CreateRecommendationValidator
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.domain.recommendation.entities.recommendation import Recommendation
from app.domain.assessment.identifiers.assessment_id import AssessmentId


class CreateRecommendationHandler:
    """Create a Recommendation aggregate and persist it."""

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, command: CreateRecommendationCommand) -> RecommendationDTO:
        validation = CreateRecommendationValidator().validate(command)
        if not validation.success:
            raise ValueError(validation.errors)

        recommendation = Recommendation(
            assessment_id=AssessmentId(command.assessment_id),
            executive_summary="Recommendation generated successfully.",
        )

        async with self._unit_of_work:
            await self._unit_of_work.recommendation_repository.add(recommendation)
            await self._unit_of_work.commit()

        return RecommendationMapper.domain_to_dto(recommendation)
