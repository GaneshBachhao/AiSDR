"""
Email value object.

Represents a validated contact email address.
"""

from __future__ import annotations

import re


class Email:
    """
    Immutable value object representing email address.

    Business rules:
    - Email is mandatory.
    - Email cannot be empty.
    - Email is normalized.
    - Email format must be valid.
    """

    _EMAIL_PATTERN = re.compile(
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    )

    def __init__(
        self,
        value: str,
    ) -> None:

        normalized = value.strip().lower()

        self._validate(normalized)

        self._value = normalized

    @property
    def value(self) -> str:
        return self._value

    def _validate(
        self,
        value: str,
    ) -> None:

        if not value:
            raise ValueError(
                "Email cannot be empty."
            )

        if not self._EMAIL_PATTERN.match(value):
            raise ValueError(
                "Invalid email format."
            )

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return (
            f"Email('{self.value}')"
        )

    def __eq__(
        self,
        other: object,
    ) -> bool:

        if not isinstance(other, Email):
            return False

        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)