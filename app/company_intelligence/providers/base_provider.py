"""
Base Company Intelligence Provider

Defines the interface for all company
intelligence providers.
"""

from abc import ABC, abstractmethod

from app.lead_intelligence.schemas.lead_candidate_schema import (
    LeadCandidate,
)

from app.company_intelligence.schemas.company_profile_schema import (
    CompanyProfile,
)


class BaseCompanyIntelligenceProvider(ABC):
    """
    Base provider interface.
    """

    @abstractmethod
    def enrich(
        self,
        candidate: LeadCandidate,
    ) -> CompanyProfile:
        """
        Build a CompanyProfile from a LeadCandidate.
        """
        raise NotImplementedError