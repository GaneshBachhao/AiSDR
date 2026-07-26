import pytest

from app.application.recommendation.commands.add_solution import (
    AddSolutionCommand,
)
from app.application.recommendation.handlers.add_solution_handler import (
    AddSolutionHandler,
)
from app.application.recommendation.mappers.recommendation_mapper import (
    RecommendationMapper,
)
from app.application.recommendation.validators.add_solution_validator import (
    AddSolutionValidator,
)

from app.domain.recommendation.enums.solution_type import (
    SolutionType,
)
from app.domain.recommendation.enums.implementation_priority import (
    ImplementationPriority,
)

from tests.application.recommendation.fakes.fake_recommendation_repository import (
    FakeRecommendationRepository,
)


@pytest.mark.asyncio
async def test_add_solution_handler_adds_solution():

    repository = FakeRecommendationRepository()

    handler = AddSolutionHandler(
        repository=repository,
        validator=AddSolutionValidator(),
        mapper=RecommendationMapper(),
    )

    command = AddSolutionCommand(
        recommendation_id=repository.recommendation.id.value,
        title="AI Sales Assistant",
        description="Automate lead qualification.",
        solution_type=SolutionType.AI_AGENT.name,
        priority=ImplementationPriority.HIGH.name,
    )

    result = await handler.handle(
        command,
    )

    assert len(repository.recommendation.solutions) == 1

    solution = repository.recommendation.solutions[0]

    assert solution.title == "AI Sales Assistant"
    assert solution.description == "Automate lead qualification."
    assert solution.solution_type == SolutionType.AI_AGENT
    assert solution.priority == ImplementationPriority.HIGH

    assert result.id == repository.recommendation.id.value