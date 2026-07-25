import pytest

from app.application.recommendation.commands.update_cost_estimate import (
    UpdateCostEstimateCommand,
)
from app.application.recommendation.handlers.update_cost_estimate_handler import (
    UpdateCostEstimateHandler,
)
from app.application.recommendation.mappers.recommendation_mapper import (
    RecommendationMapper,
)
from app.application.recommendation.validators.update_cost_estimate_validator import (
    UpdateCostEstimateValidator,
)
from app.domain.assessment.identifiers.assessment_id import (
    AssessmentId,
)
from app.domain.recommendation.entities.recommendation import (
    Recommendation,
)
from app.domain.recommendation.entities.solution import (
    Solution,
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


class FakeRecommendationRepository(
    RecommendationRepository,
):

    def __init__(self):

        self.recommendation = Recommendation(
            assessment_id=AssessmentId(),
        )

        self.recommendation.add_solution(
            Solution(
                title="AI Sales Assistant",
                description="Automate sales qualification.",
                solution_type=SolutionType.AI_AGENT,
            )
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
async def test_update_cost_estimate_handler_updates_cost():

    repository = FakeRecommendationRepository()

    handler = UpdateCostEstimateHandler(
        repository=repository,
        validator=UpdateCostEstimateValidator(),
        mapper=RecommendationMapper(),
    )

    solution = repository.recommendation.solutions[0]

    command = UpdateCostEstimateCommand(
        recommendation_id=repository.recommendation.id.value,
        solution_id=solution.solution_id,
        estimated_cost=50000,
        currency="USD",
    )

    result = await handler.handle(
        command,
    )

    assert (
        result.id
        == repository.recommendation.id.value
    )

    updated_solution = (
        repository.recommendation.solutions[0]
    )

    assert updated_solution.cost_estimate is not None

    assert (
        updated_solution.cost_estimate.amount
        == 50000
    )

    assert (
        updated_solution.cost_estimate.currency.value
        == "USD"
    )