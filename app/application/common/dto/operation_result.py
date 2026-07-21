# app/application/common/dto/operation_result.py

"""
Standard application operation result wrapper.
"""

from __future__ import annotations

from typing import Generic, TypeVar

from app.application.common.dto.base_dto import BaseDTO

T = TypeVar("T")


class OperationResult(BaseDTO, Generic[T]):
    """
    Represents the outcome of an application operation.
    """

    success: bool

    data: T | None = None

    message: str | None = None

    metadata: dict[str, object] = {}

    @classmethod
    def succeeded(
        cls,
        data: T | None = None,
        *,
        message: str | None = None,
        metadata: dict[str, object] | None = None,
    ) -> OperationResult[T]:
        """
        Create a successful result.
        """
        return cls(
            success=True,
            data=data,
            message=message,
            metadata=metadata or {},
        )

    @classmethod
    def failed(
        cls,
        message: str,
        *,
        metadata: dict[str, object] | None = None,
    ) -> OperationResult[T]:
        """
        Create a failed result.
        """
        return cls(
            success=False,
            message=message,
            metadata=metadata or {},
        )