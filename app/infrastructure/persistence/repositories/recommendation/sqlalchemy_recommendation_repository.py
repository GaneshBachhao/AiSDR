"""SQLAlchemy Recommendation repository."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.contracts.repositories.recommendation_repository import RecommendationRepository
from app.domain.assessment.identifiers.assessment_id import AssessmentId
from app.domain.recommendation.entities.recommendation import Recommendation
from app.domain.recommendation.identifiers.recommendation_id import RecommendationId
from app.infrastructure.persistence.mappers.recommendation_mapper import RecommendationMapper
from app.infrastructure.persistence.models.recommendation_model import RecommendationModel
from app.infrastructure.persistence.repositories.base.sqlalchemy_repository import SqlAlchemyRepository


class SqlAlchemyRecommendationRepository(
    SqlAlchemyRepository[Recommendation, RecommendationModel, RecommendationId],
    RecommendationRepository,
):
    """SQLAlchemy implementation of RecommendationRepository."""

    model_type = RecommendationModel

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, mapper=RecommendationMapper())

    async def get_by_assessment_id(
        self,
        assessment_id: AssessmentId,
    ) -> Recommendation | None:
        result = await self._session.execute(
            select(RecommendationModel).where(
                RecommendationModel.assessment_id == assessment_id.value,
            )
        )
        model = result.scalar_one_or_none()
        return None if model is None else self.mapper.to_domain(model)

    async def list(
        self,
        page: int = 1,
        page_size: int = 10,
    ) -> list[Recommendation]:
        offset = (page - 1) * page_size
        result = await self._session.execute(
            select(RecommendationModel)
            .order_by(RecommendationModel.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        return [self.mapper.to_domain(model) for model in result.scalars().all()]
