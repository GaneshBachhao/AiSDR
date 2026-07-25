from __future__ import annotations

from app.domain.common.enums.currency import Currency

from app.application.common.exceptions.validation_exception import (
    ValidationException,
)
from app.application.recommendation.commands.update_cost_estimate import (
    UpdateCostEstimateCommand,
)
from app.application.recommendation.dto.recommendation_dto import (
    RecommendationDTO,
)
from app.application.recommendation.mappers.recommendation_mapper import (
    RecommendationMapper,
)
from app.application.recommendation.validators.update_cost_estimate_validator import (
    UpdateCostEstimateValidator,
)
from app.domain.recommendation.identifiers.recommendation_id import (
    RecommendationId,
)
from app.domain.recommendation.repositories.recommendation_repository import (
    RecommendationRepository,
)
from app.domain.recommendation.value_objects.cost_estimate import (
    CostEstimate,
)


class UpdateCostEstimateHandler:
    """
    Handles updating cost estimate information for a solution.
    """

    def __init__(
        self,
        repository: RecommendationRepository,
        validator: UpdateCostEstimateValidator,
        mapper: RecommendationMapper,
    ) -> None:

        self._repository = repository
        self._validator = validator
        self._mapper = mapper

    async def handle(
        self,
        command: UpdateCostEstimateCommand,
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

        cost_estimate = CostEstimate(
            amount=command.estimated_cost,
            currency=Currency(
                command.currency,
            ),
        )

        solution.update_cost_estimate(
            cost_estimate,
        )

        recommendation = await self._repository.save(
            recommendation,
        )

        return self._mapper.to_dto(
            recommendation,
        )