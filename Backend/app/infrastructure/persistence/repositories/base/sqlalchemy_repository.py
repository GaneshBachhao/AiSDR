"""
Generic SQLAlchemy repository.

The repository is persistence-generic:
- application/domain code supplies typed identifiers;
- the converter registry translates them to database values;
- concrete repositories own aggregate-specific queries.
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.common.interfaces.repository import Repository
from app.infrastructure.persistence.mappers.converter_registry import (
    converter_registry,
)

TEntity = TypeVar("TEntity")
TModel = TypeVar("TModel")
TId = TypeVar("TId")


class SqlAlchemyRepository(
    Repository[TEntity, TId],
    Generic[TEntity, TModel, TId],
):
    """Generic SQLAlchemy CRUD implementation."""

    model_type: type[TModel]

    def __init__(self, session: AsyncSession, mapper: object) -> None:
        self._session = session
        self.mapper = mapper

    async def get_by_id(self, entity_id: TId) -> TEntity | None:
        db_id = converter_registry.to_database(entity_id)

        result = await self._session.execute(select(self.model_type).where(self.model_type.id == db_id))
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self.mapper.to_domain(model)

    async def add(self, entity: TEntity) -> None:
        model = self.mapper.to_model(entity)
        self._session.add(model)

    async def update(self, entity: TEntity) -> None:
        model = self.mapper.to_model(entity)
        await self._session.merge(model)

    async def delete(self, entity_id: TId | Any) -> None:
        """Delete by typed identifier, accepting an entity for compatibility."""
        value = getattr(entity_id, "id", entity_id)
        db_id = converter_registry.to_database(value)
        model = await self._session.get(self.model_type, db_id)

        if model is not None:
            await self._session.delete(model)

    async def exists(self, entity_id: TId) -> bool:
        db_id = converter_registry.to_database(entity_id)

        result = await self._session.execute(select(self.model_type.id).where(self.model_type.id == db_id))
        return result.scalar_one_or_none() is not None
