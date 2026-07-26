from uuid import uuid4

import pytest

from app.application.recommendation.commands.create_recommendation import (
    CreateRecommendationCommand,
)
from app.application.recommendation.handlers.create_recommendation_handler import (
    CreateRecommendationHandler,
)
from app.application.recommendation.mappers.recommendation_mapper import (
    RecommendationMapper,
)
from app.application.recommendation.validators.create_recommendation_validator import (
    CreateRecommendationValidator,
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

        self.recommendation: Recommendation | None = None

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

        return self.recommendation is not None

    async def delete(
        self,
        recommendation: Recommendation,
    ) -> None:

        return None


@pytest.mark.asyncio
async def test_create_recommendation_handler_creates_recommendation():

    repository = FakeRecommendationRepository()

    handler = CreateRecommendationHandler(
        repository=repository,
        validator=CreateRecommendationValidator(),
        mapper=RecommendationMapper(),
    )

    assessment_id = uuid4()

    command = CreateRecommendationCommand(
        assessment_id=assessment_id,
    )

    result = await handler.handle(command)

    assert result.assessment_id == assessment_id
    assert result.status == "Draft"

    assert repository.recommendation is not None