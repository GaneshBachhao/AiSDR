import pytest

from app.application.recommendation.handlers.get_recommendation_handler import (
    GetRecommendationHandler,
)
from app.application.recommendation.mappers.recommendation_mapper import (
    RecommendationMapper,
)
from app.application.recommendation.queries.get_recommendation_by_id import (
    GetRecommendationByIdQuery,
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

    async def get_by_id(
        self,
        recommendation_id: RecommendationId,
    ) -> Recommendation | None:

        if (
            recommendation_id.value
            == self.recommendation.id.value
        ):
            return self.recommendation

        return None

    async def save(
        self,
        recommendation: Recommendation,
    ) -> Recommendation:

        self.recommendation = recommendation

        return recommendation

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
async def test_get_recommendation_handler_returns_recommendation():

    repository = FakeRecommendationRepository()

    handler = GetRecommendationHandler(
        repository=repository,
        mapper=RecommendationMapper(),
    )

    query = GetRecommendationByIdQuery(
        recommendation_id=repository.recommendation.id.value,
    )

    result = await handler.handle(
        query,
    )

    assert (
        result.id
        == repository.recommendation.id.value
    )

    assert (
        result.assessment_id
        == repository.recommendation.assessment_id.value
    )