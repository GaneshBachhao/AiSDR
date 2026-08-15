"""
Base application handler.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import TypeVar

from app.application.common.commands.command import (
    Command,
)

TCommand = TypeVar("TCommand", bound=Command)
TResponse = TypeVar("TResponse")


class BaseHandler(
    Generic[TCommand, TResponse],
    ABC,
):
    """
    Base class for all application handlers.
    """

    @abstractmethod
    async def handle(
        self,
        command: TCommand,
    ) -> TResponse:
        """
        Execute application use case.
        """
        raise NotImplementedError