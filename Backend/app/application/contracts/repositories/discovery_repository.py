"""
Discovery repository contract.

Architecture Freeze v5.0
"""

from __future__ import annotations

from abc import abstractmethod

from app.application.common.interfaces.repository import Repository
from app.domain.discovery.entities.discovery import Discovery
from app.domain.discovery.identifiers.discovery_id import DiscoveryId
from app.domain.lead.identifiers.lead_id import LeadId


class DiscoveryRepository(Repository[Discovery, DiscoveryId]):
    """Persistence contract for the Discovery aggregate."""

    @abstractmethod
    async def get_by_lead(self, lead_id: LeadId) -> Discovery | None:
        """Retrieve the discovery associated with a lead."""
        raise NotImplementedError

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 100) -> list[Discovery]:
        """Retrieve discoveries with pagination."""
        raise NotImplementedError

    @abstractmethod
    async def search(
        self,
        search_text: str,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Discovery]:
        """Search discovery text fields with pagination."""
        raise NotImplementedError
