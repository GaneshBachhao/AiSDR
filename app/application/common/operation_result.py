from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class OperationResult(Generic[T]):
    """
    Represents application operation result.
    """

    success: bool
    data: T | None = None
    error: str | None = None
    errors: list[str] = field(default_factory=list)

    def add_error(
        self,
        error: str,
    ) -> None:
        """
        Adds an error while preserving the first error
        as the primary error.
        """
        self.errors.append(error)

        if self.error is None:
            self.error = error

    @classmethod
    def succeeded(
        cls,
        data: T | None = None,
    ) -> "OperationResult[T]":
        return cls(
            success=True,
            data=data,
        )

    @classmethod
    def failed(
        cls,
        error: str,
    ) -> "OperationResult[T]":
        return cls(
            success=False,
            error=error,
            errors=[error],
        )