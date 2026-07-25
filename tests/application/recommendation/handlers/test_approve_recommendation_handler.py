import pytest

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

        # Recommendation lifecycle:
        # DRAFT -> UNDER_REVIEW -> APPROVED
        self.recommendation.submit_for_review()

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
async def test_approve_recommendation_handler_approves_recommendation():

    repository = FakeRecommendationRepository()

    handler = ApproveRecommendationHandler(
        repository=repository,
        validator=ApproveRecommendationValidator(),
        mapper=RecommendationMapper(),
    )

    command = ApproveRecommendationCommand(
        recommendation_id=repository.recommendation.id.value,
    )

    result = await handler.handle(
        command,
    )

    assert result.status == "APPROVED"

    assert (
        repository.recommendation.status.value
        == "Approved"
    )