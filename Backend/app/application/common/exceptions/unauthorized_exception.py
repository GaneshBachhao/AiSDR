# app/application/common/exceptions/unauthorized_exception.py

"""
Unauthorized exception.

Raised when authentication is required or authentication has failed.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.application.common.exceptions.application_exception import (
    ApplicationException,
)
from app.application.common.exceptions.error_code import ErrorCode


class UnauthorizedException(ApplicationException):
    """
    Raised when authentication fails.
    """

    def __init__(
        self,
        message: str = "Authentication required.",
        *,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=ErrorCode.UNAUTHORIZED,
            details=details,
        )