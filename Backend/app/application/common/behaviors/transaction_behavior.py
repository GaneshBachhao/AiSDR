# app/application/common/behaviors/transaction_behavior.py

"""
Transaction pipeline behavior.
"""

from __future__ import annotations

from typing import Generic, TypeVar

from app.application.common.behaviors.behavior import (
    Behavior,
    NextHandler,
)
from app.application.common.interfaces.unit_of_work import (
    UnitOfWork,
)

TRequest = TypeVar("TRequest")

TResponse = TypeVar("TResponse")


class TransactionBehavior(
    Behavior[TRequest, TResponse],
    Generic[TRequest, TResponse],
):
    """
    Wraps command execution in a transaction boundary.
    """

    def __init__(
        self,
        unit_of_work: UnitOfWork,
    ) -> None:

        self._unit_of_work = unit_of_work

    async def handle(
        self,
        request: TRequest,
        next_handler: NextHandler[TRequest, TResponse],
    ) -> TResponse:

        async with self._unit_of_work:
            response = await next_handler(
                request,
            )

            await self._unit_of_work.commit()

            return response
