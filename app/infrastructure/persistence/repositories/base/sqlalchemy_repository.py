"""
Generic SQLAlchemy repository.
"""

from __future__ import annotations

from typing import Generic
from typing import TypeVar

from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.common.interfaces.repository import (
    Repository,
)


TEntity = TypeVar("TEntity")
TModel = TypeVar("TModel")
TId = TypeVar("TId")


class SqlAlchemyRepository(
    Repository[TEntity, TId],
    Generic[TEntity, TModel, TId],
):
    """
    Generic SQLAlchemy repository implementation.
    """

    model_type: type[TModel]
    mapper: object

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def get_by_id(
        self,
        entity_id: TId,
    ) -> TEntity | None:

        result = await self._session.execute(
            select(self.model_type).where(
                self.model_type.id == entity_id
            )
        )

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self.mapper.to_domain(model)

    async def add(
        self,
        entity: TEntity,
    ) -> None:

        model = self.mapper.to_model(entity)

        self._session.add(model)

    async def update(
        self,
        entity: TEntity,
    ) -> None:

        model = self.mapper.to_model(entity)

        await self._session.merge(model)

    async def delete(
        self,
        entity: TEntity,
    ) -> None:
        """
        Delete an entity.
        """

        model = self.mapper.to_model(entity)

        await self._session.delete(model)

    async def exists(
        self,
        entity_id: TId,
    ) -> bool:

        result = await self._session.execute(
            select(self.model_type.id).where(
                self.model_type.id == entity_id
            )
        )

        return result.scalar_one_or_none() is not None

    async def list(
        self,
    ) -> list[TEntity]:

        result = await self._session.execute(
            select(self.model_type)
        )

        return [
            self.mapper.to_domain(model)
            for model in result.scalars().all()
        ]