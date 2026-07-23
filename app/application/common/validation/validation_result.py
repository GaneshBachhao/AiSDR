from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ValidationError:
    """
    Represents a single validation error.
    """

    field: str
    message: str


@dataclass
class ValidationResult:
    """
    Standard application validation result.
    """

    errors: list[ValidationError] = field(
        default_factory=list
    )

    @property
    def is_valid(self) -> bool:
        """
        Indicates whether validation succeeded.
        """
        return not self.errors


    def add_error(
        self,
        field: str,
        message: str,
    ) -> None:
        """
        Add validation error.
        """

        self.errors.append(
            ValidationError(
                field=field,
                message=message,
            )
        )


    def has_errors(self) -> bool:
        """
        Returns True if any validation errors exist.
        """

        return bool(self.errors)


    def has_error(
        self,
        field: str,
    ) -> bool:
        """
        Returns True if a specific field has an error.
        """

        return any(
            error.field == field
            for error in self.errors
        )


    def error_messages(self) -> list[str]:
        """
        Returns plain validation messages.
        """

        return [
            error.message
            for error in self.errors
        ]