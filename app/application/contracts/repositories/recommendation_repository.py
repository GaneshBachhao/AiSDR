"""
Recommendation repository contract.
"""

from __future__ import annotations

from app.application.common.interfaces.repository import (
    Repository,
)
from app.domain.recommendation.entities.recommendation import (
    Recommendation,
)
from app.domain.recommendation.identifiers.recommendation_id import (
    RecommendationId,
)


class RecommendationRepository(
    Repository[Recommendation, RecommendationId],
):
    """
    Recommendation persistence contract.
    """

    pass