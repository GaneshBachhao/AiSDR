from __future__ import annotations

from app.application.common.exceptions.validation_exception import (
    ValidationException,
)
from app.application.recommendation.commands.update_roi import (
    UpdateROICommand,
)
from app.application.recommendation.dto.recommendation_dto import (
    RecommendationDTO,
)
from app.application.recommendation.mappers.recommendation_mapper import (
    RecommendationMapper,
)
from app.application.recommendation.validators.update_roi_validator import (
    UpdateROIValidator,
)
from app.domain.recommendation.identifiers.recommendation_id import (
    RecommendationId,
)
from app.domain.recommendation.repositories.recommendation_repository import (
    RecommendationRepository,
)
from app.domain.recommendation.value_objects.expected_roi import (
    ROI,
)


class UpdateROIHandler:
    """
    Handles updating ROI information for a solution.
    """

    def __init__(
        self,
        repository: RecommendationRepository,
        validator: UpdateROIValidator,
        mapper: RecommendationMapper,
    ) -> None:

        self._repository = repository
        self._validator = validator
        self._mapper = mapper

    async def handle(
        self,
        command: UpdateROICommand,
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

        solution = next(
            (
                item
                for item in recommendation.solutions
                if item.solution_id == command.solution_id
            ),
            None,
        )

        if solution is None:
            raise ValueError(
                "Solution not found."
            )

        roi_percentage = (
            command.expected_return
            / command.investment_cost
        ) * 100

        roi = ROI(
            percentage=roi_percentage,
            payback_period="12 months",
            remarks=(
                f"Expected return: {command.expected_return}, "
                f"Investment cost: {command.investment_cost}"
            ),
        )

        solution.update_roi(
            roi,
        )

        recommendation = await self._repository.save(
            recommendation,
        )

        return self._mapper.domain_to_dto(
            recommendation,
        )