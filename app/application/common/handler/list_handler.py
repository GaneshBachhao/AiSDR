"""
Base List Handler.
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


class ListHandler(
    QueryHandler[TQuery, TResponse],
    Generic[TQuery, TEntity, TResponse],
    ABC,
):
    """
    Base class for list handlers.
    """

    async def execute(
        self,
        query: TQuery,
    ) -> TResponse:
        """
        Execute list use case.
        """

        entities = await self.load_entities(
            query,
        )

        return self.to_response(
            entities,
        )

    @abstractmethod
    async def load_entities(
        self,
        query: TQuery,
    ) -> list[TEntity]:
        """
        Load entities.
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