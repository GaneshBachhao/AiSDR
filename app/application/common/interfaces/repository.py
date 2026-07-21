# app/application/common/interfaces/repository.py

"""
Repository interface contract.

Repositories abstract persistence concerns from the Application
layer. Concrete implementations belong to Infrastructure.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar


TEntity = TypeVar("TEntity")

TId = TypeVar("TId")


class Repository(ABC, Generic[TEntity, TId]):
    """
    Base repository contract.

    Feature-specific repositories should extend this interface.
    Example:

        class LeadRepository(
            Repository[Lead, UUID]
        ):
            ...
    """

    @abstractmethod
    async def get_by_id(
        self,
        entity_id: TId,
    ) -> TEntity | None:
        """
        Retrieve entity by identity.
        """
        raise NotImplementedError

    @abstractmethod
    async def add(
        self,
        entity: TEntity,
    ) -> None:
        """
        Add a new entity.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        entity: TEntity,
    ) -> None:
        """
        Update an existing entity.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        entity: TEntity,
    ) -> None:
        """
        Delete an entity.
        """
        raise NotImplementedError

    @abstractmethod
    async def exists(
        self,
        entity_id: TId,
    ) -> bool:
        """
        Check entity existence.
        """
        raise NotImplementedError