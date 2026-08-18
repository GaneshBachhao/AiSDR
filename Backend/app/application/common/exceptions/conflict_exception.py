# app/application/common/exceptions/conflict_exception.py

"""
Conflict exception.

Raised when a requested operation cannot be completed because of
a conflicting application state.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.application.common.exceptions.application_exception import (
    ApplicationException,
)
from app.application.common.exceptions.error_code import ErrorCode


class ConflictException(ApplicationException):
    """
    Raised when a resource conflict occurs.
    """

    def __init__(
        self,
        message: str,
        *,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=ErrorCode.CONFLICT,
            details=details,
        )
