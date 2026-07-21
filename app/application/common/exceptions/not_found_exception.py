# app/application/common/exceptions/not_found_exception.py

"""
Not Found exception.

Raised when an application use case cannot locate the requested
resource.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.application.common.exceptions.application_exception import (
    ApplicationException,
)
from app.application.common.exceptions.error_code import ErrorCode


class NotFoundException(ApplicationException):
    """
    Raised when a requested resource does not exist.
    """

    def __init__(
        self,
        message: str,
        *,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=ErrorCode.NOT_FOUND,
            details=details,
        )