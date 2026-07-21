# app/application/common/exceptions/validation_exception.py

"""
Validation exception.

Raised when application-level validation fails before a use case
can be executed.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.application.common.exceptions.application_exception import (
    ApplicationException,
)
from app.application.common.exceptions.error_code import ErrorCode


class ValidationException(ApplicationException):
    """
    Raised when validation fails.
    """

    def __init__(
        self,
        message: str,
        *,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=ErrorCode.VALIDATION_ERROR,
            details=details,
        )