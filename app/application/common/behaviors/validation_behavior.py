# app/application/common/behaviors/validation_behavior.py

"""
Validation pipeline behavior.
"""

from __future__ import annotations

from typing import Generic, TypeVar

from app.application.common.behaviors.behavior import (
    Behavior,
    NextHandler,
)
from app.application.common.validation.validator import (
    Validator,
)
from app.application.common.exceptions.application_exception import (
    ApplicationException,
)


TRequest = TypeVar("TRequest")

TResponse = TypeVar("TResponse")


class ValidationBehavior(
    Behavior[TRequest, TResponse],
    Generic[TRequest, TResponse],
):
    """
    Executes validation before handler execution.
    """

    def __init__(
        self,
        validator: Validator[TRequest],
    ) -> None:

        self._validator = validator

    async def handle(
        self,
        request: TRequest,
        next_handler: NextHandler[TRequest, TResponse],
    ) -> TResponse:

        result = await self._validator.validate(
            request,
        )

        if not result.is_valid:
            raise ApplicationException(
                "Request validation failed."
            )

        return await next_handler(request)