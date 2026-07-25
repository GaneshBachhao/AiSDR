import pytest

from app.application.recommendation.commands.add_solution import (
    AddSolutionCommand,
)
from app.application.recommendation.handlers.add_solution_handler import (
    AddSolutionHandler,
)
from app.application.recommendation.mappers.solution_mapper import (
    SolutionMapper,
)
from app.application.recommendation.validators.add_solution_validator import (
    AddSolutionValidator,
)
from app.domain.assessment.identifiers.assessment_id import (
    AssessmentId,
)
from app.domain.recommendation.entities.recommendation import (
    Recommendation,
)
from app.domain.recommendation.identifiers.recommendation_id import (
    RecommendationId,
)
from app.domain.recommendation.repositories.recommendation_repository import (
    RecommendationRepository,
)


class FakeRecommendationRepository(
    RecommendationRepository,
):

    def __init__(self):

        self.recommendation = Recommendation(
            assessment_id=AssessmentId(),
        )

    async def save(
        self,
        recommendation: Recommendation,
    ) -> Recommendation:

        self.recommendation = recommendation

        return recommendation

    async def get_by_id(
        self,
        recommendation_id: RecommendationId,
    ) -> Recommendation | None:

        return self.recommendation

    async def get_by_assessment(
        self,
        assessment_id: AssessmentId,
    ) -> Recommendation | None:

        return None

    async def exists(
        self,
        recommendation_id: RecommendationId,
    ) -> bool:

        return True

    async def delete(
        self,
        recommendation: Recommendation,
    ) -> None:

        return None


@pytest.mark.asyncio
async def test_add_solution_handler_adds_solution():

    repository = FakeRecommendationRepository()

    handler = AddSolutionHandler(
        repository=repository,
        validator=AddSolutionValidator(),
        mapper=SolutionMapper(),
    )

    command = AddSolutionCommand(
        recommendation_id=repository.recommendation.id.value,
        title="AI Sales Assistant",
        description="Automate lead qualification.",
        solution_type="AI_AGENT",
        priority="HIGH",
    )

    result = await handler.handle(command)

    assert result.title == "AI Sales Assistant"
    assert result.solution_type == "AI_AGENT"
    assert result.priority == "HIGH"

    assert len(
        repository.recommendation.solutions,
    ) == 1