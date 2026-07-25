"""
Discovery Domain <-> ORM mapper.
"""

from __future__ import annotations

from app.domain.discovery.entities.discovery import Discovery
from app.infrastructure.persistence.models.discovery_model import DiscoveryModel

from .base_mapper import BaseMapper
from .converter_registry import converter_registry


class DiscoveryMapper(BaseMapper[Discovery, DiscoveryModel]):
    """
    Maps Discovery aggregate to DiscoveryModel and back.
    """

    domain_type = Discovery
    model_type = DiscoveryModel

    def to_model(
        self,
        domain: Discovery,
    ) -> DiscoveryModel:

        data = self.domain_to_dict(domain)

        for key, value in data.items():
            data[key] = converter_registry.to_database(value)

        return DiscoveryModel(
            **self.copy_matching_fields(
                data,
                DiscoveryModel,
            )
        )

    def to_domain(
        self,
        model: DiscoveryModel,
    ) -> Discovery:

        data = self.model_to_dict(model)

        annotations = getattr(
            Discovery,
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
            Discovery,
        )

        return Discovery(**filtered)