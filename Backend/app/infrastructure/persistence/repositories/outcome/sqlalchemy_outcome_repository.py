"""
SQLAlchemy implementation of OutcomeRepository.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.contracts.repositories.outcome_repository import (
    OutcomeRepository,
)
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.outcome.entities.outcome_event import OutcomeEvent
from app.domain.outcome.identifiers.outcome_event_id import OutcomeEventId
from app.infrastructure.persistence.mappers.outcome_event_mapper import (
    OutcomeEventMapper,
)
from app.infrastructure.persistence.models.outcome_event_model import (
    OutcomeEventModel,
)
from app.infrastructure.persistence.repositories.base.sqlalchemy_repository import (
    SqlAlchemyRepository,
)


class SqlAlchemyOutcomeRepository(
    SqlAlchemyRepository[OutcomeEvent, OutcomeEventModel, OutcomeEventId],
    OutcomeRepository,
):
    """SQLAlchemy OutcomeEvent repository."""

    model_type = OutcomeEventModel

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, mapper=OutcomeEventMapper())

    async def list_by_lead(self, lead_id: LeadId) -> list[OutcomeEvent]:
        result = await self._session.execute(
            select(OutcomeEventModel)
            .where(OutcomeEventModel.lead_id == lead_id.value)
            .order_by(OutcomeEventModel.occurred_at.desc())
        )
        return [self.mapper.to_domain(model) for model in result.scalars().all()]

    async def list(self, skip: int = 0, limit: int = 100) -> list[OutcomeEvent]:
        result = await self._session.execute(
            select(OutcomeEventModel).order_by(OutcomeEventModel.occurred_at.desc()).offset(skip).limit(limit)
        )
        return [self.mapper.to_domain(model) for model in result.scalars().all()]
