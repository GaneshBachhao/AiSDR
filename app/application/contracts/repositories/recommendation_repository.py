"""
Recommendation repository contract.
"""

from __future__ import annotations

from abc import abstractmethod

from app.application.common.interfaces.repository import (
    Repository,
)
from app.domain.recommendation.entities.recommendation import (
    Recommendation,
)
from app.domain.recommendation.identifiers.recommendation_id import (
    RecommendationId,
)
from app.domain.lead.identifiers.lead_id import (
    LeadId,
)


class RecommendationRepository(
    Repository[
        Recommendation,
        RecommendationId,
    ],
):
    """
    Contract for Recommendation persistence.

    Generic CRUD operations are inherited from Repository.
    """

    @abstractmethod
    async def get_by_lead_id(
        self,
        lead_id: LeadId,
    ) -> Recommendation | None:
        """
        Returns the recommendation associated with a lead.
        """
        raise NotImplementedError