import pytest

from app.application.recommendation.commands.add_roadmap_phase import (
    AddRoadmapPhaseCommand,
)
from app.application.recommendation.handlers.add_roadmap_phase_handler import (
    AddRoadmapPhaseHandler,
)
from app.application.recommendation.mappers.recommendation_mapper import (
    RecommendationMapper,
)
from app.application.recommendation.validators.add_roadmap_phase_validator import (
    AddRoadmapPhaseValidator,
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
async def test_add_roadmap_phase_handler_adds_phase():

    repository = FakeRecommendationRepository()

    handler = AddRoadmapPhaseHandler(
        repository=repository,
        validator=AddRoadmapPhaseValidator(),
        mapper=RecommendationMapper(),
    )

    command = AddRoadmapPhaseCommand(
        recommendation_id=repository.recommendation.id.value,
        name="Phase 1 - Foundation",
        description="Establish AI infrastructure and data readiness.",
        sequence=1,
    )

    result = await handler.handle(
        command,
    )

    assert len(
        repository.recommendation.roadmap_phases,
    ) == 1

    assert (
        repository.recommendation.roadmap_phases[0].phase_name
        == "Phase 1 - Foundation"
    )

    assert (
        result.id
        == repository.recommendation.id.value
    )