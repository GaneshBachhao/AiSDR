"""
Assessment Domain <-> ORM mapper.
"""

from __future__ import annotations

from app.domain.assessment.entities.assessment import Assessment
from app.infrastructure.persistence.models.assessment_model import AssessmentModel

from .base_mapper import BaseMapper
from .converter_registry import converter_registry


class AssessmentMapper(BaseMapper[Assessment, AssessmentModel]):
    """
    Maps Assessment aggregate to AssessmentModel and back.
    """

    domain_type = Assessment
    model_type = AssessmentModel

    def to_model(
        self,
        domain: Assessment,
    ) -> AssessmentModel:

        data = self.domain_to_dict(domain)

        for key, value in data.items():
            data[key] = converter_registry.to_database(value)

        return AssessmentModel(**data)

    def to_domain(
        self,
        model: AssessmentModel,
    ) -> Assessment:

        data = self.model_to_dict(model)

        annotations = getattr(Assessment, "__annotations__", {})

        for field, field_type in annotations.items():

            if field in data:
                data[field] = converter_registry.to_domain(
                    field_type,
                    data[field],
                )

        filtered = self.copy_matching_fields(
            data,
            Assessment,
        )

        return Assessment(**filtered)