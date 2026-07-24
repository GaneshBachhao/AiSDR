from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.discovery.entities.discovery_session import (
    DiscoverySession,
)

from app.domain.discovery.identifiers.discovery_session_id import (
    DiscoverySessionId,
)

from app.domain.lead.identifiers.lead_id import (
    LeadId,
)


class DiscoveryRepository(ABC):
    """
    DiscoverySession persistence contract.
    """

    @abstractmethod
    async def add(
        self,
        session: DiscoverySession,
    ) -> None:
        pass

    @abstractmethod
    async def get_by_id(
        self,
        session_id: DiscoverySessionId,
    ) -> DiscoverySession | None:
        pass

    @abstractmethod
    async def get_by_lead(
        self,
        lead_id: LeadId,
    ) -> DiscoverySession | None:
        pass

    @abstractmethod
    async def update(
        self,
        session: DiscoverySession,
    ) -> None:
        pass