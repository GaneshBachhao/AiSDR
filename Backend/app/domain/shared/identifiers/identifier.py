"""
Base strongly typed identifier.

Architecture rule:
- Domain identifiers always contain a UUID.
- HTTP/application strings are converted to typed identifiers at the
  application/domain boundary.
"""

from __future__ import annotations

from abc import ABC
from uuid import UUID, uuid4


class Identifier(ABC):
    """Base class for all strongly typed UUID identifiers."""

    def __init__(self, value: UUID | str | None = None) -> None:
        if value is None:
            self._value = uuid4()
            return

        if isinstance(value, UUID):
            self._value = value
            return

        if isinstance(value, str):
            normalized = value.strip()
            if not normalized:
                raise ValueError("Identifier cannot be empty.")

            try:
                self._value = UUID(normalized)
            except ValueError as exc:
                raise ValueError(f"Invalid UUID identifier: {value!r}") from exc
            return

        raise TypeError("Identifier value must be a UUID, string UUID, or None.")

    @classmethod
    def generate(cls, value: UUID | str | None = None) -> Identifier:
        return cls(value)

    @property
    def value(self) -> UUID:
        return self._value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._value})"
