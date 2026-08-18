"""SQLAlchemy Lead repository."""

from __future__ import annotations

from sqlalchemy import String, cast, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.contracts.repositories.lead_repository import LeadRepository
from app.domain.company.identifiers.company_id import CompanyId
from app.domain.contact.identifiers.contact_id import ContactId
from app.domain.lead.entities.lead import Lead
from app.domain.lead.identifiers.lead_id import LeadId
from app.infrastructure.persistence.mappers.lead_mapper import LeadMapper
from app.infrastructure.persistence.models.lead_model import LeadModel
from app.infrastructure.persistence.repositories.base.sqlalchemy_repository import (
    SqlAlchemyRepository,
)


class SqlAlchemyLeadRepository(
    SqlAlchemyRepository[Lead, LeadModel, LeadId],
    LeadRepository,
):
    """Persistence implementation of LeadRepository."""

    model_type = LeadModel

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, mapper=LeadMapper())

    async def list(
        self,
        company_id: CompanyId | None = None,
        contact_id: ContactId | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Lead]:
        query = select(LeadModel)

        if company_id is not None:
            query = query.where(
                LeadModel.company_id == company_id.value,
            )

        if contact_id is not None:
            query = query.where(
                LeadModel.contact_id == contact_id.value,
            )

        result = await self._session.execute(
            query.order_by(LeadModel.created_at.desc()).offset(skip).limit(limit)
        )

        return [self.mapper.to_domain(model) for model in result.scalars().all()]

    async def search(
        self,
        search_text: str,
        company_id: CompanyId | None = None,
        contact_id: ContactId | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Lead]:
        """Search Lead-owned fields and relationship identifiers."""
        query = select(LeadModel)
        query_text = search_text.strip()

        if query_text:
            pattern = f"%{query_text}%"
            query = query.where(
                or_(
                    LeadModel.source.ilike(pattern),
                    LeadModel.status.ilike(pattern),
                    LeadModel.notes.ilike(pattern),
                    cast(LeadModel.company_id, String).ilike(pattern),
                    cast(LeadModel.contact_id, String).ilike(pattern),
                )
            )

        if company_id is not None:
            query = query.where(
                LeadModel.company_id == company_id.value,
            )

        if contact_id is not None:
            query = query.where(
                LeadModel.contact_id == contact_id.value,
            )

        result = await self._session.execute(
            query.order_by(LeadModel.created_at.desc()).offset(skip).limit(limit)
        )

        return [self.mapper.to_domain(model) for model in result.scalars().all()]
