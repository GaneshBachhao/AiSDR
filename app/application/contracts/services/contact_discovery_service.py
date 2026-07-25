"""
Contact discovery service contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.discovery.entities.contact import (
    Contact,
)


class ContactDiscoveryService(ABC):
    """
    External contact discovery abstraction.

    Implementations may connect to external data providers,
    enrichment systems, or AI-based discovery services.
    """

    @abstractmethod
    async def discover(
        self,
        company_name: str,
    ) -> list[Contact]:
        """
        Discover contacts for a company.
        """
        raise NotImplementedError