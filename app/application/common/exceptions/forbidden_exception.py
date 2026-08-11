# app/application/common/exceptions/forbidden_exception.py

"""
Forbidden exception.

Raised when an authenticated user is not permitted to perform the
requested operation.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.application.common.exceptions.application_exception import (
    ApplicationException,
)
from app.application.common.exceptions.error_code import ErrorCode


class ForbiddenException(ApplicationException):
    """
    Raised when authorization fails.
    """

    def __init__(
        self,
        message: str = "Access denied.",
        *,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=ErrorCode.FORBIDDEN,
            details=details,
        )