from __future__ import annotations

from app.application.common.exceptions.validation_exception import (
    ValidationException,
)
from app.application.recommendation.commands.add_solution import (
    AddSolutionCommand,
)
from app.application.recommendation.dto.solution_dto import (
    SolutionDTO,
)
from app.application.recommendation.mappers.solution_mapper import (
    SolutionMapper,
)
from app.application.recommendation.validators.add_solution_validator import (
    AddSolutionValidator,
)
from app.domain.recommendation.entities.solution import (
    Solution,
)
from app.domain.recommendation.enums.implementation_priority import (
    ImplementationPriority,
)
from app.domain.recommendation.enums.solution_type import (
    SolutionType,
)
from app.domain.recommendation.identifiers.recommendation_id import (
    RecommendationId,
)
from app.domain.recommendation.repositories.recommendation_repository import (
    RecommendationRepository,
)


class AddSolutionHandler:
    """
    Handles adding a solution to a recommendation.
    """

    def __init__(
        self,
        repository: RecommendationRepository,
        validator: AddSolutionValidator,
        mapper: SolutionMapper,
    ) -> None:
        self._repository = repository
        self._validator = validator
        self._mapper = mapper

    async def handle(
        self,
        command: AddSolutionCommand,
    ) -> SolutionDTO:

        validation = self._validator.validate(command)

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

        solution = Solution(
            title=command.title,
            description=command.description,
            solution_type=SolutionType(
                command.solution_type,
            ),
            priority=ImplementationPriority(
                command.priority,
            ),
        )

        recommendation.add_solution(
            solution,
        )

        await self._repository.save(
            recommendation,
        )

        return self._mapper.to_dto(
            solution,
        )