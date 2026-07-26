"""
SQLAlchemy implementation of RecommendationRepository.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.recommendation.entities.recommendation import (
    Recommendation,
)
from app.infrastructure.persistence.mappers.recommendation_mapper import (
    RecommendationMapper,
)
from app.infrastructure.persistence.models.recommendation_model import (
    RecommendationModel,
)
from app.infrastructure.persistence.repositories.base.sqlalchemy_repository import (
    SqlAlchemyRepository,
)


class SqlAlchemyRecommendationRepository(
    SqlAlchemyRepository[
        Recommendation,
        RecommendationModel,
        str,
    ],
):
    """
    SQLAlchemy Recommendation repository.
    """

    model_type = RecommendationModel
    mapper = RecommendationMapper()

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:

        super().__init__(
            session=session,
        )