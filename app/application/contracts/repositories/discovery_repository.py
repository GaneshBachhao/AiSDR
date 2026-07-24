from abc import ABC, abstractmethod

from app.domain.discovery.entities.discovery import Discovery
from app.domain.discovery.value_objects.discovery_id import DiscoveryId


class DiscoveryRepository(ABC):
    """
    Discovery persistence contract.
    """

    @abstractmethod
    async def add(
        self,
        discovery: Discovery
    ) -> None:
        pass

    @abstractmethod
    async def get_by_id(
        self,
        discovery_id: DiscoveryId
    ) -> Discovery | None:
        pass

    @abstractmethod
    async def update(
        self,
        discovery: Discovery
    ) -> None:
        pass