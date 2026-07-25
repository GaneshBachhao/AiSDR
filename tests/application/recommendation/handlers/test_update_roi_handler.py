import pytest

from app.application.recommendation.commands.update_roi import (
    UpdateROICommand,
)
from app.application.recommendation.handlers.update_roi_handler import (
    UpdateROIHandler,
)
from app.application.recommendation.mappers.recommendation_mapper import (
    RecommendationMapper,
)
from app.application.recommendation.validators.update_roi_validator import (
    UpdateROIValidator,
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
async def test_update_roi_handler_updates_roi():

    repository = FakeRecommendationRepository()

    handler = UpdateROIHandler(
        repository=repository,
        validator=UpdateROIValidator(),
        mapper=RecommendationMapper(),
    )

    solution = repository.recommendation.solutions[0]

    command = UpdateROICommand(
        recommendation_id=repository.recommendation.id.value,
        solution_id=solution.solution_id,
        expected_return=150000,
        investment_cost=50000,
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

    assert updated_solution.roi is not None

    assert (
        updated_solution.roi.percentage
        == 300
    )

    assert (
        updated_solution.roi.payback_period
        == "12 months"
    )