from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.discovery.entities.discovery_session import (
    DiscoverySession,
)
from app.domain.discovery.value_objects.discovery_id import (
    DiscoveryId,
)
from app.domain.lead.identifiers.lead_id import (
    LeadId,
)


class DiscoveryRepository(ABC):
    """
    Repository interface for DiscoverySession aggregate.
    """

    @abstractmethod
    def save(
        self,
        discovery_session: DiscoverySession,
    ) -> DiscoverySession:
        """
        Persist a discovery session.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(
        self,
        discovery_id: DiscoveryId,
    ) -> DiscoverySession | None:
        """
        Retrieve a discovery session by its identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_lead(
        self,
        lead_id: LeadId,
    ) -> DiscoverySession | None:
        """
        Retrieve the discovery session associated
        with a lead.
        """
        raise NotImplementedError

    @abstractmethod
    def exists(
        self,
        discovery_id: DiscoveryId,
    ) -> bool:
        """
        Check whether a discovery session exists.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        discovery_session: DiscoverySession,
    ) -> None:
        """
        Remove a discovery session.
        """
        raise NotImplementedError