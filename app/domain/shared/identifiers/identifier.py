# app/domain/shared/identifiers/identifier.py

from __future__ import annotations

from abc import ABC
from uuid import UUID, uuid4


class Identifier(ABC):
    """
    Base class for all strongly typed identifiers.

    If no UUID is supplied, a new UUID is generated automatically.
    """

    def __init__(
        self,
        value: UUID | None = None,
    ) -> None:
        self._value = value or uuid4()

    @property
    def value(self) -> UUID:
        """
        Return the underlying UUID.
        """
        return self._value

    def __eq__(
        self,
        other: object,
    ) -> bool:
        return (
            isinstance(other, self.__class__)
            and self._value == other._value
        )

    def __hash__(
        self,
    ) -> int:
        return hash(self._value)

    def __str__(
        self,
    ) -> str:
        return str(self._value)

    def __repr__(
        self,
    ) -> str:
        return (
            f"{self.__class__.__name__}"
            f"({self._value})"
        )