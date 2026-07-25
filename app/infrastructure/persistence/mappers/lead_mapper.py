"""
Lead Domain <-> ORM mapper.
"""

from __future__ import annotations

from app.domain.lead.entities.lead import Lead
from app.infrastructure.persistence.models.lead_model import LeadModel

from .base_mapper import BaseMapper
from .converter_registry import converter_registry


class LeadMapper(BaseMapper[Lead, LeadModel]):
    """
    Maps Lead aggregate to LeadModel and back.
    """

    domain_type = Lead
    model_type = LeadModel

    def to_model(
        self,
        domain: Lead,
    ) -> LeadModel:

        data = self.domain_to_dict(domain)

        for key, value in data.items():
            data[key] = converter_registry.to_database(value)

        return LeadModel(
            **self.copy_matching_fields(
                data,
                LeadModel,
            )
        )

    def to_domain(
        self,
        model: LeadModel,
    ) -> Lead:

        data = self.model_to_dict(model)

        annotations = getattr(
            Lead,
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
            Lead,
        )

        return Lead(**filtered)