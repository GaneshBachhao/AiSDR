from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class HandlerResult(Generic[T]):
    """
    Standard application handler result.

    Every application handler returns HandlerResult.
    """

    success: bool

    data: T | None = None

    message: str | None = None

    error_code: str | None = None

    errors: list[str] = field(
        default_factory=list,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    @staticmethod
    def ok(
        data: T | None = None,
        message: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> HandlerResult[T]:
        """
        Successful execution.
        """

        return HandlerResult(
            success=True,
            data=data,
            message=message,
            metadata=metadata or {},
        )

    @staticmethod
    def failure(
        message: str,
        *,
        error_code: str | None = None,
        errors: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> HandlerResult[T]:
        """
        Failed execution.
        """

        return HandlerResult(
            success=False,
            message=message,
            error_code=error_code,
            errors=errors or [],
            metadata=metadata or {},
        )

    @property
    def has_errors(self) -> bool:
        """
        Whether execution contains errors.
        """

        return bool(self.errors)

    @property
    def is_success(self) -> bool:
        """
        Compatibility alias for the older handler contract.
        """

        return self.success

    def ensure_success(
        self,
    ) -> None:
        """
        Raise ValueError when execution failed.
        """

        if not self.success:
            raise ValueError(
                self.message or "Handler execution failed.",
            )

    def unwrap(
        self,
    ) -> T:
        """
        Return data when successful.
        """

        self.ensure_success()

        return self.data
