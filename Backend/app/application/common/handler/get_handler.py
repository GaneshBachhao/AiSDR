"""
Base Get Handler.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import TypeVar

from app.application.common.handler.query_handler import (
    QueryHandler,
)

TQuery = TypeVar("TQuery")
TEntity = TypeVar("TEntity")
TResponse = TypeVar("TResponse")


class GetHandler(
    QueryHandler[TQuery, TResponse],
    Generic[TQuery, TEntity, TResponse],
    ABC,
):
    """
    Base class for get handlers.
    """

    async def execute(
        self,
        query: TQuery,
    ) -> TResponse:
        """
        Execute get use case.
        """

        entity = await self.load_entity(
            query,
        )

        return self.to_response(
            entity,
        )

    @abstractmethod
    async def load_entity(
        self,
        query: TQuery,
    ) -> TEntity:
        """
        Load entity.
        """
        raise NotImplementedError

    @abstractmethod
    def to_response(
        self,
        entity: TEntity,
    ) -> TResponse:
        """
        Convert entity into response DTO.
        """
        raise NotImplementedError