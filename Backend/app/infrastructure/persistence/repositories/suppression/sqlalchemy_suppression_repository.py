"""
SQLAlchemy implementation of SuppressionRepository.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.contracts.repositories.suppression_repository import (
    SuppressionRepository,
)
from app.domain.suppression.entities.suppression_entry import SuppressionEntry
from app.domain.suppression.identifiers.suppression_entry_id import SuppressionEntryId
from app.infrastructure.persistence.mappers.suppression_entry_mapper import (
    SuppressionEntryMapper,
)
from app.infrastructure.persistence.models.suppression_entry_model import (
    SuppressionEntryModel,
)
from app.infrastructure.persistence.repositories.base.sqlalchemy_repository import (
    SqlAlchemyRepository,
)


class SqlAlchemySuppressionRepository(
    SqlAlchemyRepository[SuppressionEntry, SuppressionEntryModel, SuppressionEntryId],
    SuppressionRepository,
):
    """SQLAlchemy SuppressionEntry repository."""

    model_type = SuppressionEntryModel

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, mapper=SuppressionEntryMapper())

    async def find_by_email(self, email: str) -> SuppressionEntry | None:
        result = await self._session.execute(
            select(SuppressionEntryModel).where(SuppressionEntryModel.email == email.strip().lower())
        )
        model = result.scalar_one_or_none()
        return None if model is None else self.mapper.to_domain(model)

    async def list(self, skip: int = 0, limit: int = 100) -> list[SuppressionEntry]:
        result = await self._session.execute(
            select(SuppressionEntryModel)
            .order_by(SuppressionEntryModel.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return [self.mapper.to_domain(model) for model in result.scalars().all()]
