# app/application/common/behaviors/pipeline.py

"""
Application execution pipeline.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Generic, TypeVar

from app.application.common.behaviors.behavior import (
    Behavior,
)

TRequest = TypeVar("TRequest")

TResponse = TypeVar("TResponse")


Handler = Callable[
    [TRequest],
    Awaitable[TResponse],
]


class Pipeline(
    Generic[TRequest, TResponse],
):
    """
    Executes request handlers through behaviors.
    """

    def __init__(
        self,
        behaviors: list[Behavior[TRequest, TResponse]],
    ) -> None:

        self._behaviors = behaviors

    async def execute(
        self,
        request: TRequest,
        handler: Handler[TRequest, TResponse],
    ) -> TResponse:
        """
        Execute request pipeline.
        """

        async def invoke(
            index: int,
        ) -> TResponse:

            if index == len(self._behaviors):
                return await handler(request)

            behavior = self._behaviors[index]

            return await behavior.handle(
                request,
                lambda _: invoke(index + 1),
            )

        return await invoke(0)
