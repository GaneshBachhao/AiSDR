"""
SQLAlchemy Qualification repository.

Architecture Freeze v5.0
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.contracts.repositories.qualification_repository import QualificationRepository
from app.domain.assessment.identifiers.assessment_id import AssessmentId
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.qualification.entities.qualification import Qualification
from app.domain.qualification.identifiers.qualification_id import QualificationId
from app.infrastructure.persistence.mappers.qualification_mapper import QualificationPersistenceMapper
from app.infrastructure.persistence.models.qualification_model import QualificationModel
from app.infrastructure.persistence.repositories.base.sqlalchemy_repository import SqlAlchemyRepository


class SQLAlchemyQualificationRepository(
    SqlAlchemyRepository[Qualification, QualificationModel, QualificationId],
    QualificationRepository,
):
    """SQLAlchemy implementation of the Qualification repository."""

    model_type = QualificationModel

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            session=session,
            mapper=QualificationPersistenceMapper(),
        )

    async def get_by_lead_id(self, lead_id: LeadId) -> Qualification | None:
        result = await self._session.execute(
            select(QualificationModel).where(
                QualificationModel.lead_id == lead_id.value,
            )
        )
        model = result.scalar_one_or_none()
        return None if model is None else self.mapper.to_domain(model)

    async def get_by_assessment_id(
        self,
        assessment_id: AssessmentId,
    ) -> Qualification | None:
        result = await self._session.execute(
            select(QualificationModel).where(
                QualificationModel.assessment_id == assessment_id.value,
            )
        )
        model = result.scalar_one_or_none()
        return None if model is None else self.mapper.to_domain(model)

    async def list(
        self,
        page: int = 1,
        page_size: int = 10,
        lead_id: LeadId | None = None,
        assessment_id: AssessmentId | None = None,
    ) -> list[Qualification]:
        offset = (page - 1) * page_size

        query = select(QualificationModel)

        if lead_id is not None:
            query = query.where(QualificationModel.lead_id == lead_id.value)

        if assessment_id is not None:
            query = query.where(
                QualificationModel.assessment_id == assessment_id.value,
            )

        result = await self._session.execute(
            query.order_by(QualificationModel.created_at.desc()).offset(offset).limit(page_size)
        )

        return [self.mapper.to_domain(model) for model in result.scalars().all()]
