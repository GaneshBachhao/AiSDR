"""
Unit Of Work abstraction.

Architecture Freeze v5.0

The UnitOfWork is a shared application boundary.

IMPORTANT:
- Canonical repository properties use the *_repository convention.
- Legacy aggregate properties are retained for backward compatibility.
- Both names MUST resolve to the same repository instance.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.application.contracts.repositories.assessment_repository import (
    AssessmentRepository,
)
from app.application.contracts.repositories.company_repository import (
    CompanyRepository,
)
from app.application.contracts.repositories.contact_repository import (
    ContactRepository,
)
from app.application.contracts.repositories.discovery_repository import (
    DiscoveryRepository,
)
from app.application.contracts.repositories.lead_repository import (
    LeadRepository,
)
from app.application.contracts.repositories.qualification_repository import (
    QualificationRepository,
)
from app.application.contracts.repositories.recommendation_repository import (
    RecommendationRepository,
)
from app.application.contracts.repositories.user_repository import (
    UserRepository,
)


class UnitOfWork(ABC):
    """
    Application-level Unit of Work contract.

    All repositories participating in a use case share the same
    transaction boundary.

    Canonical repository access:
        company_repository
        contact_repository
        lead_repository
        discovery_repository
        assessment_repository
        qualification_repository

    Compatibility access:
        companies
        contacts
        leads
        discoveries
        assessments
        qualifications
    """

    # ==========================================================
    # Canonical repository contract
    # ==========================================================

    @property
    @abstractmethod
    def company_repository(self) -> CompanyRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def contact_repository(self) -> ContactRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def lead_repository(self) -> LeadRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def discovery_repository(self) -> DiscoveryRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def assessment_repository(self) -> AssessmentRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def qualification_repository(
        self,
    ) -> QualificationRepository:
        raise NotImplementedError

    # ==========================================================
    # Backward-compatible repository aliases
    # ==========================================================

    @property
    def companies(self) -> CompanyRepository:
        """
        Backward-compatible alias for company_repository.
        """
        return self.company_repository

    @property
    def contacts(self) -> ContactRepository:
        """
        Backward-compatible alias for contact_repository.
        """
        return self.contact_repository

    @property
    def leads(self) -> LeadRepository:
        """
        Backward-compatible alias for lead_repository.
        """
        return self.lead_repository

    @property
    def discoveries(self) -> DiscoveryRepository:
        """
        Backward-compatible alias for discovery_repository.
        """
        return self.discovery_repository

    @property
    def assessments(self) -> AssessmentRepository:
        """
        Backward-compatible alias for assessment_repository.
        """
        return self.assessment_repository

    @property
    def qualifications(self) -> QualificationRepository:
        """
        Backward-compatible alias for qualification_repository.
        """
        return self.qualification_repository

    @property
    def recommendation_repository(self) -> RecommendationRepository:
        """Recommendation repository; optional for legacy UoW implementations."""
        raise NotImplementedError

    @property
    def recommendations(self) -> RecommendationRepository:
        """Backward-compatible alias for recommendation_repository."""
        return self.recommendation_repository

    @property
    def user_repository(self) -> UserRepository:
        """User repository; optional for legacy UoW implementations."""
        raise NotImplementedError

    # ==========================================================
    # Transaction boundary
    # ==========================================================

    @abstractmethod
    async def __aenter__(self) -> UnitOfWork:
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
