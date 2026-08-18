"""
Base Create Handler.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from app.application.common.commands.command import (
    Command,
)
from app.application.common.handler.command_handler import (
    CommandHandler,
)

TCommand = TypeVar(
    "TCommand",
    bound=Command,
)

TEntity = TypeVar("TEntity")

TResponse = TypeVar("TResponse")


class CreateHandler(
    CommandHandler[TCommand, TResponse],
    Generic[TCommand, TEntity, TResponse],
    ABC,
):
    """
    Base class for create handlers.
    """

    async def execute(
        self,
        command: TCommand,
    ) -> TResponse:
        """
        Execute create use case.
        """

        entity = await self.create_entity(
            command,
        )

        await self.before_persist(
            entity,
        )

        await self.persist(
            entity,
        )

        await self.after_persist(
            entity,
        )

        return self.to_response(
            entity,
        )

    async def before_persist(
        self,
        entity: TEntity,
    ) -> None:
        """
        Hook before persistence.
        """
        return None

    async def after_persist(
        self,
        entity: TEntity,
    ) -> None:
        """
        Hook after persistence.
        """
        return None

    @abstractmethod
    async def create_entity(
        self,
        command: TCommand,
    ) -> TEntity:
        """
        Create domain entity.
        """
        raise NotImplementedError

    @abstractmethod
    async def persist(
        self,
        entity: TEntity,
    ) -> None:
        """
        Persist entity.
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
