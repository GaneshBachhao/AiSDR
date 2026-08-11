# app/application/common/exceptions/application_exception.py

"""
Base application exception.

Application exceptions represent failures during application
orchestration and use-case execution. They must not be used for
domain business rule violations.
"""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Any

from app.application.common.exceptions.error_code import ErrorCode


class ApplicationException(Exception):
    """
    Base class for all application-layer exceptions.
    """

    def __init__(
        self,
        message: str,
        *,
        error_code: ErrorCode = ErrorCode.INTERNAL_ERROR,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message)

        self._message = message
        self._error_code = error_code
        self._details = MappingProxyType(dict(details or {}))

    @property
    def message(self) -> str:
        """
        Human-readable error message.
        """
        return self._message

    @property
    def error_code(self) -> ErrorCode:
        """
        Stable application error code.
        """
        return self._error_code

    @property
    def details(self) -> Mapping[str, Any]:
        """
        Read-only structured metadata.
        """
        return self._details

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the exception into a structured payload.
        """
        return {
            "message": self.message,
            "error_code": self.error_code.value,
            "details": dict(self.details),
        }

    def __str__(self) -> str:
        return self.message