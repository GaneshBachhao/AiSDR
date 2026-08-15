from __future__ import annotations

from app.domain.assessment.identifiers.assessment_id import (
    AssessmentId,
)
from app.domain.recommendation.entities.recommendation import (
    Recommendation,
)
from app.domain.recommendation.repositories.recommendation_repository import (
    RecommendationRepository,
)


class FakeRecommendationRepository(
    RecommendationRepository,
):
    """
    In-memory Recommendation repository used by
    application handler tests.
    """

    def __init__(
        self,
        recommendation: Recommendation | None = None,
    ) -> None:

        self.recommendation = (
            recommendation
            or Recommendation(
                assessment_id=AssessmentId(),
            )
        )

        self.saved_recommendation: Recommendation | None = None
        self.updated_recommendation: Recommendation | None = None
        self.deleted_recommendation: Recommendation | None = None

    async def save(
        self,
        recommendation: Recommendation,
    ) -> Recommendation:

        self.saved_recommendation = recommendation
        self.recommendation = recommendation

        return recommendation

    async def update(
        self,
        recommendation: Recommendation,
    ) -> Recommendation:

        self.updated_recommendation = recommendation
        self.recommendation = recommendation

        return recommendation

    async def delete(
        self,
        recommendation: Recommendation,
    ) -> None:

        self.deleted_recommendation = recommendation

        if (
            self.recommendation.id.value
            == recommendation.id.value
        ):
            self.recommendation = None

    async def get_by_id(
        self,
        recommendation_id,
    ) -> Recommendation | None:

        if self.recommendation is None:
            return None

        if (
            self.recommendation.id.value
            == recommendation_id
        ):
            return self.recommendation

        return None

    async def get_by_assessment(
        self,
        assessment_id,
    ) -> Recommendation | None:

        if self.recommendation is None:
            return None

        if (
            self.recommendation.assessment_id.value
            == assessment_id
        ):
            return self.recommendation

        return None

    async def exists(
        self,
        recommendation_id,
    ) -> bool:

        recommendation = await self.get_by_id(
            recommendation_id,
        )

        return recommendation is not None