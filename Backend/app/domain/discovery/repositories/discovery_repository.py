"""
Discovery repository contract.
"""

from __future__ import annotations

from abc import abstractmethod

from app.application.common.interfaces.repository import Repository
from app.domain.discovery.entities.discovery import Discovery
from app.domain.discovery.identifiers.discovery_id import DiscoveryId
from app.domain.lead.identifiers.lead_id import LeadId


class DiscoveryRepository(
    Repository[Discovery, DiscoveryId],
):
    """
    Repository contract for Discovery aggregate.

    Provides generic CRUD operations through the base
    Repository interface and exposes only aggregate-
    specific queries here.
    """

    @abstractmethod
    async def get_by_lead(
        self,
        lead_id: LeadId,
    ) -> Discovery | None:
        """
        Retrieve the discovery associated with a lead.
        """
        raise NotImplementedError