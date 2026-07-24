from abc import ABC, abstractmethod

from app.domain.discovery.entities.contact import Contact


class ContactDiscoveryService(ABC):
    """
    External contact discovery abstraction.
    """

    @abstractmethod
    async def discover(
        self,
        company_name: str
    ) -> list[Contact]:
        pass