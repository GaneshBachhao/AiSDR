"""
SQLAlchemy implementation of CompanyRepository.
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.contracts.repositories.company_repository import (
    CompanyRepository,
)
from app.domain.company.entities.company import Company
from app.domain.company.identifiers.company_id import CompanyId
from app.infrastructure.persistence.mappers.company_mapper import CompanyMapper
from app.infrastructure.persistence.models.company_model import CompanyModel
from app.infrastructure.persistence.repositories.base.sqlalchemy_repository import (
    SqlAlchemyRepository,
)


class SqlAlchemyCompanyRepository(
    SqlAlchemyRepository[Company, CompanyModel, CompanyId],
    CompanyRepository,
):
    """SQLAlchemy Company repository."""

    model_type = CompanyModel

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, mapper=CompanyMapper())

    async def find_by_name(self, name: str) -> Company | None:
        result = await self._session.execute(
            select(CompanyModel).where(
                CompanyModel.name == name.strip()
            )
        )
        model = result.scalar_one_or_none()
        return None if model is None else self.mapper.to_domain(model)

    async def list(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Company]:
        result = await self._session.execute(
            select(CompanyModel)
            .where(CompanyModel.is_deleted.is_(False))
            .order_by(CompanyModel.name.asc())
            .offset(skip)
            .limit(limit)
        )
        return [
            self.mapper.to_domain(model)
            for model in result.scalars().all()
        ]

    async def search(
        self,
        search_text: str,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Company]:
        query_text = search_text.strip()
        if not query_text:
            return await self.list(skip=skip, limit=limit)

        result = await self._session.execute(
            select(CompanyModel)
            .where(
                CompanyModel.is_deleted.is_(False),
                CompanyModel.name.ilike(f"%{query_text}%"),
            )
            .order_by(CompanyModel.name.asc())
            .offset(skip)
            .limit(limit)
        )
        return [
            self.mapper.to_domain(model)
            for model in result.scalars().all()
        ]

    async def update(self, entity: Company) -> None:
        """
        Update the already-persisted ORM row in place.

        This avoids merging a newly-created ORM instance with missing
        server-managed timestamp/audit fields.
        """
        db_id = entity.id.value
        model = await self._session.get(CompanyModel, db_id)

        if model is None:
            return

        self.mapper.update_model(model, entity)
