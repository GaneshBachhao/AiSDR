# app/application/common/exceptions/error_code.py

"""
Application error codes.

Defines the canonical error codes used throughout the application
layer. These codes provide stable identifiers for API responses,
logging, telemetry, and client integrations.
"""

from enum import StrEnum


class ErrorCode(StrEnum):
    """
    Standard application error codes.
    """

    VALIDATION_ERROR = "VALIDATION_ERROR"

    NOT_FOUND = "NOT_FOUND"

    CONFLICT = "CONFLICT"

    UNAUTHORIZED = "UNAUTHORIZED"

    FORBIDDEN = "FORBIDDEN"

    INTERNAL_ERROR = "INTERNAL_ERROR"