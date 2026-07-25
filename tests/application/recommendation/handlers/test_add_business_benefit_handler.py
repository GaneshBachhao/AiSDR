import pytest

from app.application.recommendation.commands.add_business_benefit import (
    AddBusinessBenefitCommand,
)
from app.application.recommendation.handlers.add_business_benefit_handler import (
    AddBusinessBenefitHandler,
)
from app.application.recommendation.mappers.recommendation_mapper import (
    RecommendationMapper,
)
from app.application.recommendation.validators.add_business_benefit_validator import (
    AddBusinessBenefitValidator,
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
                description="Automate lead qualification.",
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
async def test_add_business_benefit_handler_adds_benefit():

    repository = FakeRecommendationRepository()

    handler = AddBusinessBenefitHandler(
        repository=repository,
        validator=AddBusinessBenefitValidator(),
        mapper=RecommendationMapper(),
    )

    solution = repository.recommendation.solutions[0]

    command = AddBusinessBenefitCommand(
        recommendation_id=repository.recommendation.id.value,
        solution_id=solution.solution_id,
        title="Revenue Growth",
        description="Increase qualified sales opportunities.",
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

    assert len(
        updated_solution.business_benefits,
    ) == 1

    benefit = updated_solution.business_benefits[0]

    assert benefit.title == "Revenue Growth"

    assert (
        benefit.description
        == "Increase qualified sales opportunities."
    )