"""
Validation Result

Represents the outcome of a validation operation.
"""

from dataclasses import dataclass, field
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar


T = TypeVar("T")


@dataclass(slots=True)
class ValidationResult(Generic[T]):
    """
    Result returned by every validator.

    Attributes
    ----------
    is_valid
        Indicates whether validation succeeded.

    validated_value
        The validated (and optionally normalized) value.

    errors
        Validation errors.

    warnings
        Non-blocking validation warnings.
    """

    is_valid: bool

    validated_value: Optional[T] = None

    errors: List[str] = field(default_factory=list)

    warnings: List[str] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        """
        Returns True if validation errors exist.
        """
        return bool(self.errors)

    @property
    def has_warnings(self) -> bool:
        """
        Returns True if validation warnings exist.
        """
        return bool(self.warnings)

    @classmethod
    def success(
        cls,
        value: Optional[T] = None,
    ) -> "ValidationResult[T]":
        """
        Create a successful validation result.
        """
        return cls(
            is_valid=True,
            validated_value=value,
        )

    @classmethod
    def failure(
        cls,
        *errors: str,
    ) -> "ValidationResult[T]":
        """
        Create a failed validation result.
        """
        return cls(
            is_valid=False,
            errors=list(errors),
        )

    def add_warning(
        self,
        warning: str,
    ) -> None:
        """
        Add a validation warning.
        """
        self.warnings.append(warning)

    def add_error(
        self,
        error: str,
    ) -> None:
        """
        Add a validation error.
        """
        self.errors.append(error)
        self.is_valid = False