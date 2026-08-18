"""
Discovery domain <-> ORM mapper.

Architecture Freeze v5.0
"""

from __future__ import annotations

from app.domain.discovery.entities.discovery import Discovery
from app.domain.discovery.enums.discovery_status import DiscoveryStatus
from app.domain.discovery.identifiers.discovery_id import DiscoveryId
from app.domain.lead.identifiers.lead_id import LeadId
from app.infrastructure.persistence.models.discovery_model import DiscoveryModel


class DiscoveryMapper:
    """Map the Discovery aggregate to and from persistence."""

    @staticmethod
    def _to_status(
        value: str | DiscoveryStatus,
    ) -> DiscoveryStatus:
        """
        Convert the persisted status into the domain enum.
        """
        if isinstance(value, DiscoveryStatus):
            return value

        try:
            return DiscoveryStatus(value)
        except ValueError as exc:
            raise ValueError(f"Invalid discovery status: {value!r}") from exc

    def to_model(
        self,
        domain: Discovery,
    ) -> DiscoveryModel:
        """
        Convert Discovery domain entity into ORM model.
        """
        return DiscoveryModel(
            id=domain.id.value,
            lead_id=domain.lead_id.value,
            summary=domain.problem_statement,
            current_process=domain.current_solution,
            challenges=domain.business_impact,
            goals=domain.success_criteria,
            status=domain.status.value,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
        )

    def to_domain(
        self,
        model: DiscoveryModel,
    ) -> Discovery:
        """
        Convert Discovery ORM model into domain entity.
        """
        return Discovery(
            id=DiscoveryId(model.id),
            lead_id=LeadId(model.lead_id),
            problem_statement=model.summary,
            current_solution=model.current_process,
            business_impact=model.challenges,
            success_criteria=model.goals,
            status=self._to_status(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
