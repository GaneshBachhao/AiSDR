from app.application.recommendation.commands.add_solution import (
    AddSolutionCommand,
)

from app.application.recommendation.mappers.recommendation_mapper import (
    RecommendationMapper,
)
from app.domain.recommendation.entities.solution import Solution

class AddSolutionHandler:
    """
    Adds a solution to recommendation.
    """

    def __init__(
        self,
        repository,
        validator,
        mapper: RecommendationMapper,
    ):
        self._repository = repository
        self._validator = validator
        self._mapper = mapper


    async def handle(
        self,
        command: AddSolutionCommand,
    ):

        validation = self._validator.validate(
            command
        )

        if not validation.success:
            raise ValueError(
                validation.errors
            )

        recommendation = await self._repository.get_by_id(
            command.recommendation_id
        )

        if recommendation is None:
            raise ValueError(
                "Recommendation not found."
            )

        solution = Solution(
            title=command.title,
            description=command.description,
            solution_type=command.solution_type,
            priority=command.priority,
        )

        recommendation.add_solution(
            solution
        )

        await self._repository.update(
            recommendation
        )

        return self._mapper.domain_to_dto(
            recommendation
        )