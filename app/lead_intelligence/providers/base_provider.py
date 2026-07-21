"""
Base Lead Provider

Defines the contract that every lead source
must implement.

Examples:

- Manual Provider
- CSV Provider
- Website Provider
- Search Provider
- CRM Provider
"""

from abc import ABC, abstractmethod

from app.lead_intelligence.schemas.lead_candidate_schema import (
    LeadCandidate,
)

from app.lead_intelligence.schemas.lead_search_request_schema import (
    LeadSearchRequest,
)


class BaseLeadProvider(ABC):
    """
    Base contract for all lead providers.
    """

    @abstractmethod
    def search(
        self,
        request: LeadSearchRequest,
    ) -> list[LeadCandidate]:
        """
        Search for lead candidates.

        Returns:
            List of LeadCandidate objects.
        """
        pass