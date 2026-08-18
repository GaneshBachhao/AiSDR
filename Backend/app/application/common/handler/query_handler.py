"""
Base Query Handler.

Provides the common execution pipeline for all query handlers
(Get, List, Search).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from app.application.common.handler.base_handler import (
    BaseHandler,
)

TQuery = TypeVar("TQuery")
TResponse = TypeVar("TResponse")


class QueryHandler(
    BaseHandler[TQuery, TResponse],
    Generic[TQuery, TResponse],
    ABC,
):
    """
    Base execution pipeline for queries.
    """

    def __init__(
        self,
        validator=None,
    ) -> None:
        self._validator = validator

    async def handle(
        self,
        query: TQuery,
    ) -> TResponse:
        """
        Execute query.
        """

        await self.before_validate(
            query,
        )

        await self.validate(
            query,
        )

        await self.after_validate(
            query,
        )

        return await self.execute(
            query,
        )

    async def before_validate(
        self,
        query: TQuery,
    ) -> None:
        """
        Hook executed before validation.
        """
        return None

    async def validate(
        self,
        query: TQuery,
    ) -> None:
        """
        Validate query.
        """
        if self._validator is not None:
            await self._validator.validate(
                query,
            )

    async def after_validate(
        self,
        query: TQuery,
    ) -> None:
        """
        Hook executed after validation.
        """
        return None

    @abstractmethod
    async def execute(
        self,
        query: TQuery,
    ) -> TResponse:
        """
        Execute business logic.
        """
        raise NotImplementedError
