import pytest

from tests.application.recommendation.fakes.fake_recommendation_repository import (
    FakeRecommendationRepository,
)

from app.application.recommendation.commands.submit_recommendation import (
    SubmitRecommendationCommand,
)

from app.application.recommendation.handlers.submit_recommendation_handler import (
    SubmitRecommendationHandler,
)

from app.application.recommendation.mappers.recommendation_mapper import (
    RecommendationMapper,
)

from app.application.recommendation.validators.submit_recommendation_validator import (
    SubmitRecommendationValidator,
)

from app.domain.recommendation.entities.solution import (
    Solution,
)

from app.domain.recommendation.enums.solution_type import (
    SolutionType,
)


@pytest.mark.asyncio
async def test_submit_recommendation_handler_submits_for_review():

    repository = FakeRecommendationRepository()

    # -----------------------------------------------------------------
    # Recommendation must contain at least one solution before submit.
    # -----------------------------------------------------------------
    repository.recommendation.add_solution(
        Solution(
            title="AI Sales Assistant",
            description="Automate lead qualification.",
            solution_type=SolutionType.AI_AGENT,
        )
    )

    handler = SubmitRecommendationHandler(
        repository=repository,
        validator=SubmitRecommendationValidator(),
        mapper=RecommendationMapper(),
    )

    command = SubmitRecommendationCommand(
        recommendation_id=repository.recommendation.id.value,
    )

    result = await handler.handle(command)

    assert result.status == "Under Review"

    assert (
        repository.recommendation.status.value
        == "Under Review"
    )

    assert repository.updated_recommendation is not None