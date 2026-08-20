"""SQLAlchemy Sequence repository."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.contracts.repositories.sequence_repository import (
    SequenceRepository,
)
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.sequence.entities.sequence import Sequence
from app.domain.sequence.identifiers.sequence_id import SequenceId
from app.infrastructure.persistence.mappers.sequence_mapper import SequenceMapper
from app.infrastructure.persistence.models.sequence_model import SequenceModel
from app.infrastructure.persistence.repositories.base.sqlalchemy_repository import (
    SqlAlchemyRepository,
)


class SqlAlchemySequenceRepository(
    SqlAlchemyRepository[Sequence, SequenceModel, SequenceId],
    SequenceRepository,
):
    """Persistence implementation of SequenceRepository."""

    model_type = SequenceModel

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, mapper=SequenceMapper())

    async def update(self, entity: Sequence) -> None:
        """
        Update the already-persisted ORM row in place.

        Same fix as SqlAlchemyLeadRepository: the generic base update()
        (`session.merge(mapper.to_model(entity))`) merges a
        freshly-constructed model that never sets the BaseModel
        audit-mixin columns, and would additionally rebuild the touches
        relationship from scratch on every save even though touches never
        change after creation. mapper.update_model() only ever touches
        Sequence's own scalar fields.
        """
        model = await self._session.get(SequenceModel, entity.id.value)

        if model is None:
            return

        self.mapper.update_model(model, entity)

    async def list_by_lead(self, lead_id: LeadId) -> list[Sequence]:
        result = await self._session.execute(
            select(SequenceModel)
            .where(SequenceModel.lead_id == lead_id.value)
            .order_by(SequenceModel.created_at.desc())
        )
        return [self.mapper.to_domain(model) for model in result.scalars().all()]
