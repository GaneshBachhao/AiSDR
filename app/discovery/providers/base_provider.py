from abc import ABC, abstractmethod

from app.discovery.schemas.discovery_schema import DiscoveryResult


class BaseDiscoveryProvider(ABC):
    """
    Base interface for all lead discovery providers.
    """

    @abstractmethod
    def discover(
        self,
        industry: str,
        location: str,
        max_results: int = 10
    ) -> list[DiscoveryResult]:
        """
        Discover companies matching the search criteria.

        Args:
            industry: Target industry
            location: Target location
            max_results: Maximum companies to return

        Returns:
            List of discovered companies.
        """
        pass