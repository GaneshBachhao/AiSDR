"""
AI Request Domain <-> ORM mapper.
"""

from __future__ import annotations

from app.domain.ai.aggregates.ai_request import AIRequest
from app.infrastructure.persistence.models.ai_request_model import (
    AIRequestModel,
)

from .base_mapper import BaseMapper
from .converter_registry import converter_registry


class AIRequestMapper(BaseMapper[AIRequest, AIRequestModel]):
    """
    Maps AIRequest domain entity to AIRequestModel and back.
    """

    domain_type = AIRequest
    model_type = AIRequestModel

    def to_model(
        self,
        domain: AIRequest,
    ) -> AIRequestModel:

        data = self.domain_to_dict(domain)

        for key, value in data.items():
            data[key] = converter_registry.to_database(value)

        return AIRequestModel(
            **self.copy_matching_fields(
                data,
                AIRequestModel,
            )
        )

    def to_domain(
        self,
        model: AIRequestModel,
    ) -> AIRequest:

        data = self.model_to_dict(model)

        annotations = getattr(
            AIRequest,
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
            AIRequest,
        )

        return AIRequest(**filtered)
