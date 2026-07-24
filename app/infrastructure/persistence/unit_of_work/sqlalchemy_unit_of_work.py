"""
SQLAlchemy Unit of Work.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.persistence.repositories.ai.sqlalchemy_ai_request_repository import (
    SqlAlchemyAIRequestRepository,
)
from app.infrastructure.persistence.repositories.assessment.sqlalchemy_assessment_repository import (
    SqlAlchemyAssessmentRepository,
)
from app.infrastructure.persistence.repositories.discovery.sqlalchemy_discovery_repository import (
    SqlAlchemyDiscoveryRepository,
)
from app.infrastructure.persistence.repositories.lead.sqlalchemy_lead_repository import (
    SqlAlchemyLeadRepository,
)
from app.infrastructure.persistence.repositories.recommendation.sqlalchemy_recommendation_repository import (
    SqlAlchemyRecommendationRepository,
)

from .base_unit_of_work import BaseUnitOfWork


class SqlAlchemyUnitOfWork(BaseUnitOfWork):
    """
    SQLAlchemy implementation of Unit of Work.
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:

        self._session = session

        self.leads = SqlAlchemyLeadRepository(session)
        self.assessments = SqlAlchemyAssessmentRepository(session)
        self.discoveries = SqlAlchemyDiscoveryRepository(session)
        self.recommendations = SqlAlchemyRecommendationRepository(session)
        self.ai_requests = SqlAlchemyAIRequestRepository(session)

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type,
        exc,
        tb,
    ) -> None:

        if exc:
            await self.rollback()
        else:
            await self.commit()

        await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()