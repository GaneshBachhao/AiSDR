import pytest

from app.application.recommendation.commands.add_dependency import (
    AddDependencyCommand,
)
from app.application.recommendation.handlers.add_dependency_handler import (
    AddDependencyHandler,
)
from app.application.recommendation.mappers.recommendation_mapper import (
    RecommendationMapper,
)
from app.application.recommendation.validators.add_dependency_validator import (
    AddDependencyValidator,
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
async def test_add_dependency_handler_adds_dependency():

    repository = FakeRecommendationRepository()

    handler = AddDependencyHandler(
        repository=repository,
        validator=AddDependencyValidator(),
        mapper=RecommendationMapper(),
    )

    solution = repository.recommendation.solutions[0]

    command = AddDependencyCommand(
        recommendation_id=repository.recommendation.id.value,
        solution_id=solution.solution_id,
        name="CRM Data Access",
        description="Requires access to existing CRM customer data.",
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
        updated_solution.dependencies,
    ) == 1

    dependency = updated_solution.dependencies[0]

    assert dependency.name == "CRM Data Access"

    assert (
        dependency.description
        == "Requires access to existing CRM customer data."
    )