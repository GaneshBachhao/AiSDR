"""
Repository supporting specifications.
"""

from __future__ import annotations

from typing import Generic
from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .sqlalchemy_repository import SqlAlchemyRepository

TEntity = TypeVar("TEntity")
TModel = TypeVar("TModel")
TId = TypeVar("TId")


class SpecificationRepository(
    SqlAlchemyRepository[
        TEntity,
        TModel,
        TId,
    ],
    Generic[TEntity, TModel, TId],
):
    """
    SQLAlchemy repository supporting specifications.
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:

        super().__init__(session)

    async def find(
        self,
        specification,
    ) -> list[TEntity]:

        query = specification.apply(
            select(self.model_type)
        )

        result = await self._session.execute(query)

        return [
            self.mapper.to_domain(model)
            for model in result.scalars().all()
        ]