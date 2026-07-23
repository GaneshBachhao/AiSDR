from dataclasses import dataclass
from typing import Generic, Optional, TypeVar


T = TypeVar("T")


@dataclass
class OperationResult(Generic[T]):
    """
    Represents application operation result.
    """

    success: bool

    data: Optional[T] = None

    error: Optional[str] = None


    @classmethod
    def succeeded(
        cls,
        data: T | None = None,
    ):
        return cls(
            success=True,
            data=data,
        )


    @classmethod
    def failed(
        cls,
        error: str,
    ):
        return cls(
            success=False,
            error=error,
        )