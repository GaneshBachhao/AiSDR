"""
Repository abstraction.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TEntity = TypeVar("TEntity")
TId = TypeVar("TId")


class BaseRepository(ABC, Generic[TEntity, TId]):
    """
    Base repository contract.
    """

    @abstractmethod
    async def get_by_id(
        self,
        entity_id: TId,
    ) -> TEntity | None:
        """
        Returns an entity by id.
        """

    @abstractmethod
    async def add(
        self,
        entity: TEntity,
    ) -> None:
        """
        Adds a new entity.
        """

    @abstractmethod
    async def update(
        self,
        entity: TEntity,
    ) -> None:
        """
        Updates an entity.
        """

    @abstractmethod
    async def delete(
        self,
        entity_id: TId,
    ) -> None:
        """
        Deletes an entity.
        """

    @abstractmethod
    async def exists(
        self,
        entity_id: TId,
    ) -> bool:
        """
        Checks whether an entity exists.
        """

    @abstractmethod
    async def list(
        self,
    ) -> list[TEntity]:
        """
        Returns all entities.
        """
