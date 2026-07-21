from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.assessment.value_objects.assessment_id import (
    AssessmentId,
)
from app.domain.recommendation.entities.recommendation import (
    Recommendation,
)
from app.domain.recommendation.value_objects.recommendation_id import (
    RecommendationId,
)


class RecommendationRepository(ABC):
    """
    Repository interface for the Recommendation aggregate.
    """

    @abstractmethod
    def save(
        self,
        recommendation: Recommendation,
    ) -> Recommendation:
        """
        Persist a recommendation.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(
        self,
        recommendation_id: RecommendationId,
    ) -> Recommendation | None:
        """
        Retrieve a recommendation by its identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_assessment(
        self,
        assessment_id: AssessmentId,
    ) -> Recommendation | None:
        """
        Retrieve the recommendation associated with an assessment.
        """
        raise NotImplementedError

    @abstractmethod
    def exists(
        self,
        recommendation_id: RecommendationId,
    ) -> bool:
        """
        Determine whether a recommendation exists.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        recommendation: Recommendation,
    ) -> None:
        """
        Remove a recommendation.
        """
        raise NotImplementedError