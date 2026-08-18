# app/application/common/behaviors/logging_behavior.py

"""
Logging pipeline behavior.

Actual logging implementation belongs to Infrastructure.
"""

from __future__ import annotations

from typing import Generic, TypeVar

from app.application.common.behaviors.behavior import (
    Behavior,
    NextHandler,
)

TRequest = TypeVar("TRequest")

TResponse = TypeVar("TResponse")


class LoggingBehavior(
    Behavior[TRequest, TResponse],
    Generic[TRequest, TResponse],
):
    """
    Logging pipeline placeholder.

    Logging infrastructure will be connected later through
    application ports.
    """

    async def handle(
        self,
        request: TRequest,
        next_handler: NextHandler[TRequest, TResponse],
    ) -> TResponse:

        return await next_handler(request)
