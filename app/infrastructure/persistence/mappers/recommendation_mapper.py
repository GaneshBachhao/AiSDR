"""Recommendation domain <-> ORM mapper."""

from __future__ import annotations

from app.domain.assessment.identifiers.assessment_id import AssessmentId
from app.domain.recommendation.entities.recommendation import Recommendation
from app.domain.recommendation.enums.recommendation_status import RecommendationStatus
from app.domain.recommendation.identifiers.recommendation_id import RecommendationId
from app.infrastructure.persistence.models.recommendation_model import RecommendationModel


class RecommendationMapper:
    """Map Recommendation aggregates to and from the existing table."""

    @staticmethod
    def to_model(domain: Recommendation) -> RecommendationModel:
        return RecommendationModel(
            id=domain.id.value,
            assessment_id=domain.assessment_id.value,
            summary=domain.executive_summary or "",
            created_at=domain.created_at,
            updated_at=domain.updated_at,
        )

    @staticmethod
    def to_domain(model: RecommendationModel) -> Recommendation:
        recommendation = Recommendation(
            id=RecommendationId(model.id),
            assessment_id=AssessmentId(model.assessment_id),
            status=RecommendationStatus.DRAFT,
            executive_summary=model.summary,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
        return recommendation
