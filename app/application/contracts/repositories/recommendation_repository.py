from abc import ABC, abstractmethod

from app.domain.recommendation.entities.recommendation import Recommendation
from app.domain.recommendation.value_objects.recommendation_id import RecommendationId


class RecommendationRepository(ABC):
    """
    Recommendation persistence contract.
    """

    @abstractmethod
    async def add(
        self,
        recommendation: Recommendation
    ) -> None:
        pass

    @abstractmethod
    async def get_by_id(
        self,
        recommendation_id: RecommendationId
    ) -> Recommendation | None:
        pass

    @abstractmethod
    async def update(
        self,
        recommendation: Recommendation
    ) -> None:
        pass