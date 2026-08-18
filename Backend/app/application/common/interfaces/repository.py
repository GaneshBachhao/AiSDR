"""
Repository interface contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TEntity = TypeVar("TEntity")
TId = TypeVar("TId")


class Repository(ABC, Generic[TEntity, TId]):
    """Base repository contract."""

    @abstractmethod
    async def get_by_id(self, entity_id: TId) -> TEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def add(self, entity: TEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: TEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity_id: TId) -> None:
        raise NotImplementedError

    @abstractmethod
    async def exists(self, entity_id: TId) -> bool:
        raise NotImplementedError
