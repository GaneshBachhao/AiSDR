"""
Validation Error

Exception raised when validation cannot continue.
"""

from typing import Optional


class ValidationError(Exception):
    """
    Exception raised for validation failures that
    should immediately stop execution.
    """

    def __init__(
        self,
        message: str,
        *,
        field: Optional[str] = None,
    ) -> None:
        super().__init__(message)

        self.message = message
        self.field = field

    def __str__(self) -> str:
        """
        Human-readable representation.
        """
        if self.field:
            return f"{self.field}: {self.message}"

        return self.message