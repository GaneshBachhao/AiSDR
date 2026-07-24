from abc import ABC, abstractmethod

from app.domain.recommendation.entities.recommendation import Recommendation


class RecommendationService(ABC):
    """
    Recommendation workflow contract.
    """

    @abstractmethod
    async def generate(
        self,
        recommendation: Recommendation
    ) -> Recommendation:
        pass