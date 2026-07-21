"""
Configuration Result

Represents the outcome of a configuration lookup.
"""

from dataclasses import dataclass
from typing import Generic
from typing import Optional
from typing import TypeVar


T = TypeVar("T")


@dataclass(slots=True)
class ConfigurationResult(Generic[T]):
    """
    Result returned by configuration operations.

    Attributes
    ----------
    success
        Indicates whether the configuration value
        was successfully resolved.

    value
        The resolved configuration value.

    source
        The configuration source
        (environment, yaml, json, etc.).

    error
        Error message if resolution failed.
    """

    success: bool

    value: Optional[T] = None

    source: Optional[str] = None

    error: Optional[str] = None

    @property
    def has_value(self) -> bool:
        """
        Returns True if a configuration value exists.
        """
        return self.value is not None

    @classmethod
    def success_result(
        cls,
        value: T,
        *,
        source: Optional[str] = None,
    ) -> "ConfigurationResult[T]":
        """
        Create a successful configuration result.
        """
        return cls(
            success=True,
            value=value,
            source=source,
        )

    @classmethod
    def failure(
        cls,
        error: str,
    ) -> "ConfigurationResult[T]":
        """
        Create a failed configuration result.
        """
        return cls(
            success=False,
            error=error,
        )