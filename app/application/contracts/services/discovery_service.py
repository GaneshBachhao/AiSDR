from abc import ABC, abstractmethod

from app.domain.discovery.entities.discovery import Discovery


class DiscoveryService(ABC):
    """
    Discovery workflow contract.
    """

    @abstractmethod
    async def execute(
        self,
        discovery: Discovery
    ) -> Discovery:
        pass