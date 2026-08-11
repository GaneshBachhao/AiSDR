"""
SQLAlchemy Unit of Work.

Architecture Freeze v5.0

Active Aggregates:
- Company
- Contact
- Lead
- Discovery
- Assessment
- Qualification

All repositories share one AsyncSession and therefore one
transaction boundary.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.application.common.interfaces.unit_of_work import (
    UnitOfWork,
)
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

from app.infrastructure.persistence.repositories.assessment.sqlalchemy_assessment_repository import (
    SqlAlchemyAssessmentRepository,
)
from app.infrastructure.persistence.repositories.company.sqlalchemy_company_repository import (
    SqlAlchemyCompanyRepository,
)
from app.infrastructure.persistence.repositories.contact.sqlalchemy_contact_repository import (
    SqlAlchemyContactRepository,
)
from app.infrastructure.persistence.repositories.discovery.sqlalchemy_discovery_repository import (
    SqlAlchemyDiscoveryRepository,
)
from app.infrastructure.persistence.repositories.lead.sqlalchemy_lead_repository import (
    SqlAlchemyLeadRepository,
)
from app.infrastructure.persistence.repositories.qualification.sqlalchemy_qualification_repository import (
    SQLAlchemyQualificationRepository,
)
from app.infrastructure.persistence.repositories.recommendation.sqlalchemy_recommendation_repository import (
    SqlAlchemyRecommendationRepository,
)


class SqlAlchemyUnitOfWork(UnitOfWork):
    """
    SQLAlchemy implementation of the application Unit of Work.

    Every repository is constructed with the same AsyncSession.

    This guarantees that operations performed through different
    repositories participate in the same transaction.
    """

    def __init__(
        self,
        session: AsyncSession | async_sessionmaker[AsyncSession],
    ) -> None:
        self._session_factory: async_sessionmaker[AsyncSession] | None = None
        self.session: AsyncSession | None = None

        if isinstance(session, AsyncSession):
            self.session = session
        else:
            self._session_factory = session

        self._initialize_repositories()

    def _initialize_repositories(self) -> None:
        """Create all repositories against the active session."""
        if self.session is None:
            return

        session = self.session

        self._company_repository = SqlAlchemyCompanyRepository(
            session=session,
        )
        self._contact_repository = SqlAlchemyContactRepository(
            session=session,
        )
        self._lead_repository = SqlAlchemyLeadRepository(
            session=session,
        )
        self._discovery_repository = SqlAlchemyDiscoveryRepository(
            session=session,
        )
        self._assessment_repository = SqlAlchemyAssessmentRepository(
            session=session,
        )
        self._qualification_repository = SQLAlchemyQualificationRepository(
            session=session,
        )
        self._recommendation_repository = SqlAlchemyRecommendationRepository(
            session=session,
        )

    # ==========================================================
    # Canonical repository properties
    # ==========================================================

    @property
    def company_repository(
        self,
    ) -> CompanyRepository:
        return self._company_repository

    @property
    def contact_repository(
        self,
    ) -> ContactRepository:
        return self._contact_repository

    @property
    def lead_repository(
        self,
    ) -> LeadRepository:
        return self._lead_repository

    @property
    def discovery_repository(
        self,
    ) -> DiscoveryRepository:
        return self._discovery_repository

    @property
    def assessment_repository(
        self,
    ) -> AssessmentRepository:
        return self._assessment_repository

    @property
    def qualification_repository(
        self,
    ) -> QualificationRepository:
        return self._qualification_repository

    @property
    def recommendation_repository(
        self,
    ) -> RecommendationRepository:
        return self._recommendation_repository

    # ==========================================================
    # Backward-compatible aliases
    #
    # DO NOT create new repository instances here.
    # These return the exact same instances above.
    # ==========================================================

    @property
    def companies(self) -> CompanyRepository:
        return self._company_repository

    @property
    def contacts(self) -> ContactRepository:
        return self._contact_repository

    @property
    def leads(self) -> LeadRepository:
        return self._lead_repository

    @property
    def discoveries(self) -> DiscoveryRepository:
        return self._discovery_repository

    @property
    def assessments(self) -> AssessmentRepository:
        return self._assessment_repository

    @property
    def qualifications(self) -> QualificationRepository:
        return self._qualification_repository

    @property
    def recommendations(self) -> RecommendationRepository:
        return self._recommendation_repository

    # ==========================================================
    # Context manager
    # ==========================================================

    async def __aenter__(
        self,
    ) -> SqlAlchemyUnitOfWork:
        if self.session is None:
            if self._session_factory is None:
                raise RuntimeError("Unit of Work has no session source.")
            self.session = self._session_factory()
            self._initialize_repositories()

        return self

    async def __aexit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        try:
            if exc_type is not None:
                await self.rollback()
            else:
                await self.commit()
        finally:
            if self._session_factory is not None and self.session is not None:
                await self.session.close()
                self.session = None

    # ==========================================================
    # Transaction control
    # ==========================================================

    async def commit(self) -> None:
        if self.session is None:
            raise RuntimeError("Unit of Work is not active.")
        await self.session.commit()

    async def rollback(self) -> None:
        if self.session is None:
            raise RuntimeError("Unit of Work is not active.")
        await self.session.rollback()
