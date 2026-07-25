from __future__ import annotations

from app.application.recommendation.dto.recommendation_dto import (
    RecommendationDTO,
)
from app.domain.recommendation.entities.recommendation import (
    Recommendation,
)


class RecommendationMapper:
    """
    Maps Recommendation aggregates to DTOs.
    """

    @staticmethod
    def to_dto(
        recommendation: Recommendation,
    ) -> RecommendationDTO:
        return RecommendationDTO(
            id=recommendation.id.value,
            assessment_id=recommendation.assessment_id.value,
            status=recommendation.status.name,
            created_at=recommendation.created_at,
            submitted_at=recommendation.submitted_at,
            approved_at=recommendation.approved_at,
        )