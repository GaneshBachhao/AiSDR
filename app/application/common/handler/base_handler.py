from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .handler_context import HandlerContext
from .handler_result import HandlerResult

from ..exceptions.handler_exception import (
    HandlerExecutionException,
)


RequestT = TypeVar("RequestT")
ResponseT = TypeVar("ResponseT")


class BaseHandler(
    ABC,
    Generic[RequestT, ResponseT],
):
    """
    Base class for all application handlers.

    Responsibilities
    ----------------
    - Standard execution lifecycle
    - Context validation
    - Exception translation
    """

    async def execute(
        self,
        request: RequestT,
        context: HandlerContext,
    ) -> HandlerResult[ResponseT]:
        """
        Execute the handler.
        """

        self.validate_context(context)

        try:

            return await self.handle(
                request=request,
                context=context,
            )

        except Exception as exc:

            raise HandlerExecutionException(
                message="Unexpected handler execution failure.",
                details={
                    "handler": self.__class__.__name__,
                    "exception": str(exc),
                },
            ) from exc

    @abstractmethod
    async def handle(
        self,
        request: RequestT,
        context: HandlerContext,
    ) -> HandlerResult[ResponseT]:
        """
        Execute the application use case.
        """
        ...

    def validate_context(
        self,
        context: HandlerContext,
    ) -> None:
        """
        Validate execution context.

        Override in derived handlers when additional
        context validation is required.
        """

        if context is None:

            raise HandlerExecutionException(
                message="Handler context is required.",
            )