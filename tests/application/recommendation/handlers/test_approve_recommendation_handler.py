import pytest

from tests.application.recommendation.fakes.fake_recommendation_repository import (
    FakeRecommendationRepository,
)

from app.application.recommendation.commands.approve_recommendation import (
    ApproveRecommendationCommand,
)
from app.application.recommendation.handlers.approve_recommendation_handler import (
    ApproveRecommendationHandler,
)
from app.application.recommendation.mappers.recommendation_mapper import (
    RecommendationMapper,
)
from app.application.recommendation.validators.approve_recommendation_validator import (
    ApproveRecommendationValidator,
)
from app.domain.recommendation.enums.recommendation_status import (
    RecommendationStatus,
)

from app.domain.recommendation.entities.solution import (
    Solution,
)

from app.domain.recommendation.enums.solution_type import (
    SolutionType,
)

@pytest.mark.asyncio
async def test_approve_recommendation_handler_approves_recommendation():

    repository = FakeRecommendationRepository()

    repository.recommendation.add_solution(
        Solution(
            title="AI Sales Assistant",
            description="Automate lead qualification.",
            solution_type=SolutionType.AI_AGENT,
        )
    )

    repository.recommendation.submit_for_review()

    handler = ApproveRecommendationHandler(
        repository=repository,
        validator=ApproveRecommendationValidator(),
        mapper=RecommendationMapper(),
    )

    command = ApproveRecommendationCommand(
        recommendation_id=repository.recommendation.id.value,
    )

    result = await handler.handle(command)

    assert result.status == "Approved"

    assert (
        repository.recommendation.status
        == RecommendationStatus.APPROVED
    )

    assert repository.updated_recommendation is repository.recommendation