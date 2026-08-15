"""
Base Update Handler.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import TypeVar

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


class UpdateHandler(
    CommandHandler[TCommand, TResponse],
    Generic[TCommand, TEntity, TResponse],
    ABC,
):
    """
    Base class for update handlers.
    """

    async def execute(
        self,
        command: TCommand,
    ) -> TResponse:
        """
        Execute update use case.
        """

        entity = await self.load_entity(
            command,
        )

        entity = await self.update_entity(
            entity,
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
        Hook executed before persistence.
        """
        return None

    async def after_persist(
        self,
        entity: TEntity,
    ) -> None:
        """
        Hook executed after persistence.
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
    async def update_entity(
        self,
        entity: TEntity,
        command: TCommand,
    ) -> TEntity:
        """
        Apply updates to the entity.
        """
        raise NotImplementedError

    @abstractmethod
    async def persist(
        self,
        entity: TEntity,
    ) -> None:
        """
        Persist updated entity.
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