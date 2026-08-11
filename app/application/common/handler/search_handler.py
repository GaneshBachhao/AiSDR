"""
Base Search Handler.
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


class SearchHandler(
    QueryHandler[TQuery, TResponse],
    Generic[TQuery, TEntity, TResponse],
    ABC,
):
    """
    Base class for search handlers.
    """

    async def execute(
        self,
        query: TQuery,
    ) -> TResponse:
        """
        Execute search use case.
        """

        entities = await self.search(
            query,
        )

        return self.to_response(
            entities,
        )

    @abstractmethod
    async def search(
        self,
        query: TQuery,
    ) -> list[TEntity]:
        """
        Execute search.
        """
        raise NotImplementedError

    @abstractmethod
    def to_response(
        self,
        entities: list[TEntity],
    ) -> TResponse:
        """
        Convert entities into response DTO.
        """
        raise NotImplementedError