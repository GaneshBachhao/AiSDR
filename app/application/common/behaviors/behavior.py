# app/application/common/behaviors/behavior.py

"""
Base pipeline behavior contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Awaitable, Callable, Generic, TypeVar


TRequest = TypeVar("TRequest")

TResponse = TypeVar("TResponse")


NextHandler = Callable[
    [TRequest],
    Awaitable[TResponse],
]


class Behavior(
    ABC,
    Generic[TRequest, TResponse],
):
    """
    Base behavior contract.
    """

    @abstractmethod
    async def handle(
        self,
        request: TRequest,
        next_handler: NextHandler[TRequest, TResponse],
    ) -> TResponse:
        """
        Execute behavior and continue pipeline.
        """
        raise NotImplementedError