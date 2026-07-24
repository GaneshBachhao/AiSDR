"""
Repository registrations.
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


class RepositoryProvider:
    """
    Repository factory.
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:

        self.leads = SqlAlchemyLeadRepository(session)
        self.assessments = SqlAlchemyAssessmentRepository(session)
        self.discoveries = SqlAlchemyDiscoveryRepository(session)
        self.recommendations = SqlAlchemyRecommendationRepository(session)
        self.ai_requests = SqlAlchemyAIRequestRepository(session)