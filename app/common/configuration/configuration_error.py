"""
Configuration Error

Exception raised for critical configuration failures.
"""

from typing import Optional


class ConfigurationError(Exception):
    """
    Exception raised when a configuration
    error prevents the application from
    continuing safely.
    """

    def __init__(
        self,
        message: str,
        *,
        key: Optional[str] = None,
        source: Optional[str] = None,
    ) -> None:
        super().__init__(message)

        self.message = message
        self.key = key
        self.source = source

    def __str__(self) -> str:
        """
        Human-readable representation.
        """

        parts = []

        if self.source:
            parts.append(f"[{self.source}]")

        if self.key:
            parts.append(f"{self.key}:")

        parts.append(self.message)

        return " ".join(parts)