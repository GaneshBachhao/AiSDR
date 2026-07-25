import pytest

from app.application.recommendation.commands.add_implementation_risk import (
    AddImplementationRiskCommand,
)
from app.application.recommendation.handlers.add_implementation_risk_handler import (
    AddImplementationRiskHandler,
)
from app.application.recommendation.mappers.recommendation_mapper import (
    RecommendationMapper,
)
from app.application.recommendation.validators.add_implementation_risk_validator import (
    AddImplementationRiskValidator,
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
async def test_add_implementation_risk_handler_adds_risk():

    repository = FakeRecommendationRepository()

    handler = AddImplementationRiskHandler(
        repository=repository,
        validator=AddImplementationRiskValidator(),
        mapper=RecommendationMapper(),
    )

    solution = repository.recommendation.solutions[0]

    command = AddImplementationRiskCommand(
        recommendation_id=repository.recommendation.id.value,
        solution_id=solution.solution_id,
        title="Data Quality Risk",
        description="Incomplete customer data may reduce AI accuracy.",
        mitigation="Implement data cleansing and validation pipelines.",
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
        updated_solution.implementation_risks,
    ) == 1

    risk = updated_solution.implementation_risks[0]

    assert risk.title == "Data Quality Risk"

    assert (
        risk.description
        == "Incomplete customer data may reduce AI accuracy."
    )

    assert (
        risk.mitigation
        == "Implement data cleansing and validation pipelines."
    )