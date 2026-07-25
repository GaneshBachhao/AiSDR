"""
SQLAlchemy implementation of LeadRepository.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.lead.entities.lead import Lead
from app.infrastructure.persistence.mappers.lead_mapper import LeadMapper
from app.infrastructure.persistence.models.lead_model import LeadModel
from app.infrastructure.persistence.repositories.base.sqlalchemy_repository import (
    SqlAlchemyRepository,
)


class SqlAlchemyLeadRepository(
    SqlAlchemyRepository[
        Lead,
        LeadModel,
        str,
    ],
):
    """
    SQLAlchemy Lead repository.
    """

    model_type = LeadModel
    mapper = LeadMapper()

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        super().__init__(
            session=session,
            mapper=self.mapper,
        )