from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar


TEntity = TypeVar("TEntity")
TId = TypeVar("TId")


class Repository(
    ABC,
    Generic[TEntity, TId],
):
    """
    Base repository interface for domain aggregates.

    Concrete repositories should implement persistence
    for a specific aggregate.
    """

    @abstractmethod
    def save(
        self,
        entity: TEntity,
    ) -> TEntity:
        """
        Persist an entity.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(
        self,
        entity_id: TId,
    ) -> TEntity | None:
        """
        Retrieve an entity by identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def exists(
        self,
        entity_id: TId,
    ) -> bool:
        """
        Check whether an entity exists.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        entity: TEntity,
    ) -> None:
        """
        Remove an entity.
        """
        raise NotImplementedError