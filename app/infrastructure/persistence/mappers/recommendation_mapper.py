"""
Recommendation Domain <-> ORM mapper.
"""

from __future__ import annotations

from app.domain.recommendation.entities.recommendation import Recommendation
from app.infrastructure.persistence.models.recommendation_model import (
    RecommendationModel,
)

from .base_mapper import BaseMapper
from .converter_registry import converter_registry


class RecommendationMapper(
    BaseMapper[Recommendation, RecommendationModel]
):
    """
    Maps Recommendation aggregate to RecommendationModel and back.
    """

    domain_type = Recommendation
    model_type = RecommendationModel

    def to_model(
        self,
        domain: Recommendation,
    ) -> RecommendationModel:

        data = self.domain_to_dict(domain)

        for key, value in data.items():
            data[key] = converter_registry.to_database(value)

        return RecommendationModel(
            **self.copy_matching_fields(
                data,
                RecommendationModel,
            )
        )

    def to_domain(
        self,
        model: RecommendationModel,
    ) -> Recommendation:

        data = self.model_to_dict(model)

        annotations = getattr(
            Recommendation,
            "__annotations__",
            {},
        )

        for field, field_type in annotations.items():
            if field in data:
                data[field] = converter_registry.to_domain(
                    field_type,
                    data[field],
                )

        filtered = self.copy_matching_fields(
            data,
            Recommendation,
        )

        return Recommendation(**filtered)