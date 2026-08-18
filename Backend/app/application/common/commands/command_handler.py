# app/application/common/commands/command_handler.py

"""
Command handler contract.

Each command should have exactly one handler responsible for
executing the application operation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TCommand = TypeVar(
    "TCommand",
)

TResult = TypeVar(
    "TResult",
)


class CommandHandler(
    ABC,
    Generic[TCommand, TResult],
):
    """
    Base command handler contract.
    """

    @abstractmethod
    async def handle(
        self,
        command: TCommand,
    ) -> TResult:
        """
        Execute the command.
        """
        raise NotImplementedError
