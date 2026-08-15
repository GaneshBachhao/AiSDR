from __future__ import annotations

from app.application.common.exceptions.validation_exception import (
    ValidationException,
)
from app.application.recommendation.commands.add_dependency import (
    AddDependencyCommand,
)
from app.application.recommendation.dto.recommendation_dto import (
    RecommendationDTO,
)
from app.application.recommendation.mappers.recommendation_mapper import (
    RecommendationMapper,
)
from app.application.recommendation.validators.add_dependency_validator import (
    AddDependencyValidator,
)
from app.domain.recommendation.identifiers.recommendation_id import (
    RecommendationId,
)
from app.domain.recommendation.repositories.recommendation_repository import (
    RecommendationRepository,
)
from app.domain.recommendation.value_objects.dependency import (
    Dependency,
)


class AddDependencyHandler:
    """
    Handles adding a dependency
    to a recommendation solution.
    """

    def __init__(
        self,
        repository: RecommendationRepository,
        validator: AddDependencyValidator,
        mapper: RecommendationMapper,
    ) -> None:

        self._repository = repository
        self._validator = validator
        self._mapper = mapper

    async def handle(
        self,
        command: AddDependencyCommand,
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

        dependency = Dependency(
            name=command.name,
            description=command.description,
        )

        solution.add_dependency(
            dependency,
        )

        recommendation = await self._repository.save(
            recommendation,
        )

        return self._mapper.domain_to_dto(
            recommendation,
        )