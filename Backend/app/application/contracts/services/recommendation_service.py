"""
Recommendation service contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.recommendation.entities.recommendation import (
    Recommendation,
)


class RecommendationService(ABC):
    """
    Recommendation workflow contract.

    Application layer depends on this abstraction.
    """

    @abstractmethod
    async def generate(
        self,
        recommendation: Recommendation,
    ) -> Recommendation:
        """
        Generate recommendation workflow result.
        """
        raise NotImplementedError
