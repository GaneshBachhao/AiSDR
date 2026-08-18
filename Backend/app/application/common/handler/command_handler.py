"""
Base Command Handler.

Provides the common execution pipeline for all command handlers
(Create, Update, Delete).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from app.application.common.commands.command import (
    Command,
)
from app.application.common.handler.base_handler import (
    BaseHandler,
)
from app.application.common.interfaces.unit_of_work import (
    UnitOfWork,
)

TCommand = TypeVar(
    "TCommand",
    bound=Command,
)

TResponse = TypeVar("TResponse")


class CommandHandler(
    BaseHandler[TCommand, TResponse],
    Generic[TCommand, TResponse],
    ABC,
):
    """
    Base execution pipeline for commands.
    """

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        validator=None,
    ) -> None:
        self._unit_of_work = unit_of_work
        self._validator = validator

    async def handle(
        self,
        command: TCommand,
    ) -> TResponse:
        """
        Execute command.
        """

        try:
            await self.before_validate(
                command,
            )

            await self.validate(
                command,
            )

            await self.after_validate(
                command,
            )

            response = await self.execute(
                command,
            )

            await self.before_commit()

            await self._unit_of_work.commit()

            await self.after_commit()

            return response

        except Exception:
            await self._unit_of_work.rollback()

            raise

    async def before_validate(
        self,
        command: TCommand,
    ) -> None:
        """
        Hook executed before validation.
        """
        return None

    async def validate(
        self,
        command: TCommand,
    ) -> None:
        """
        Validate command.
        """
        if self._validator is not None:
            await self._validator.validate(
                command,
            )

    async def after_validate(
        self,
        command: TCommand,
    ) -> None:
        """
        Hook executed after validation.
        """
        return None

    async def before_commit(
        self,
    ) -> None:
        """
        Hook executed before commit.
        """
        return None

    async def after_commit(
        self,
    ) -> None:
        """
        Hook executed after commit.
        """
        return None

    @abstractmethod
    async def execute(
        self,
        command: TCommand,
    ) -> TResponse:
        """
        Execute business logic.
        """
        raise NotImplementedError
