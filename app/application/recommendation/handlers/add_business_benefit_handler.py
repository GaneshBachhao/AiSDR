from __future__ import annotations

from app.application.common.exceptions.validation_exception import (
    ValidationException,
)
from app.application.recommendation.commands.add_business_benefit import (
    AddBusinessBenefitCommand,
)
from app.application.recommendation.dto.recommendation_dto import (
    RecommendationDTO,
)
from app.application.recommendation.mappers.recommendation_mapper import (
    RecommendationMapper,
)
from app.application.recommendation.validators.add_business_benefit_validator import (
    AddBusinessBenefitValidator,
)
from app.domain.recommendation.identifiers.recommendation_id import (
    RecommendationId,
)
from app.domain.recommendation.repositories.recommendation_repository import (
    RecommendationRepository,
)
from app.domain.recommendation.value_objects.business_benefit import (
    BusinessBenefit,
)


class AddBusinessBenefitHandler:
    """
    Handles adding a business benefit to a solution.
    """

    def __init__(
        self,
        repository: RecommendationRepository,
        validator: AddBusinessBenefitValidator,
        mapper: RecommendationMapper,
    ) -> None:

        self._repository = repository
        self._validator = validator
        self._mapper = mapper

    async def handle(
        self,
        command: AddBusinessBenefitCommand,
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

        benefit = BusinessBenefit(
            title=command.title,
            description=command.description,
        )

        solution.add_business_benefit(
            benefit,
        )

        recommendation = await self._repository.save(
            recommendation,
        )

        return self._mapper.domain_to_dto(
            recommendation,
        )