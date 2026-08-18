"""
Base Delete Handler.
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


class DeleteHandler(
    CommandHandler[TCommand, TResponse],
    Generic[TCommand, TEntity, TResponse],
    ABC,
):
    """
    Base class for delete handlers.
    """

    async def execute(
        self,
        command: TCommand,
    ) -> TResponse:
        """
        Execute delete use case.
        """

        entity = await self.load_entity(
            command,
        )

        await self.before_delete(
            entity,
        )

        await self.delete_entity(
            entity,
        )

        await self.after_delete(
            entity,
        )

        return self.to_response(
            entity,
        )

    async def before_delete(
        self,
        entity: TEntity,
    ) -> None:
        """
        Hook executed before delete.
        """
        return None

    async def after_delete(
        self,
        entity: TEntity,
    ) -> None:
        """
        Hook executed after delete.
        """
        return None

    @abstractmethod
    async def load_entity(
        self,
        command: TCommand,
    ) -> TEntity:
        """
        Load existing entity.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_entity(
        self,
        entity: TEntity,
    ) -> None:
        """
        Delete entity.
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
