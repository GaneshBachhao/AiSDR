"""
SQLAlchemy implementation of LeadRepository.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.lead.entities.lead import Lead
from app.domain.lead.identifiers.lead_id import LeadId

from app.infrastructure.persistence.mappers.lead_mapper import (
    LeadMapper,
)

from app.infrastructure.persistence.models.lead_model import (
    LeadModel,
)

from app.infrastructure.persistence.repositories.base.sqlalchemy_repository import (
    SqlAlchemyRepository,
)


class SqlAlchemyLeadRepository(
    SqlAlchemyRepository[
        Lead,
        LeadModel,
        LeadId,
    ],
):
    """
    SQLAlchemy Lead repository.
    """

    model_type = LeadModel
    _mapper = LeadMapper()

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        super().__init__(
            session=session,
            mapper=self._mapper,
        )

    async def find_by_email(
        self,
        email: str,
    ) -> Lead | None:

        result = await self.session.execute(
            select(LeadModel).where(
                LeadModel.email == email,
            )
        )

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self.mapper.to_domain(model)

    async def find_by_email(
        self,
        email: str,
    ) -> Lead | None:
            """
            Retrieve lead by email address.
            """

            result = await self._session.execute(
                select(LeadModel).where(
                    LeadModel.email == email,
                )
            )

            model = result.scalar_one_or_none()

            if model is None:
                return None

            return self.mapper.to_domain(model)