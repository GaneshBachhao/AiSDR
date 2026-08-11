"""Recommendation repository contract."""

from __future__ import annotations

from abc import abstractmethod

from app.application.common.interfaces.repository import Repository
from app.domain.assessment.identifiers.assessment_id import AssessmentId
from app.domain.recommendation.entities.recommendation import Recommendation
from app.domain.recommendation.identifiers.recommendation_id import RecommendationId


class RecommendationRepository(
    Repository[Recommendation, RecommendationId],
):
    """Persistence contract for Recommendation."""

    @abstractmethod
    async def get_by_assessment_id(
        self,
        assessment_id: AssessmentId,
    ) -> Recommendation | None:
        raise NotImplementedError

    @abstractmethod
    async def list(
        self,
        page: int = 1,
        page_size: int = 10,
    ) -> list[Recommendation]:
        raise NotImplementedError
