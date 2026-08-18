"""
Discovery service contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.discovery.entities.discovery import (
    Discovery,
)


class DiscoveryService(ABC):
    """
    Discovery workflow contract.

    Application layer depends on this abstraction.
    """

    @abstractmethod
    async def execute(
        self,
        discovery: Discovery,
    ) -> Discovery:
        """
        Execute discovery workflow.
        """
        raise NotImplementedError
