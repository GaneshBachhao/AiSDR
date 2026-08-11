from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from typing import Generic, TypeVar


TId = TypeVar("TId")


@dataclass(eq=False)
class Entity(
    ABC,
    Generic[TId],
):
    """
    Base class for all domain entities.

    Identity defines equality rather than attribute values.
    """

    id: TId = field(
        kw_only=True,
    )

    def __eq__(
        self,
        other: object,
    ) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.id == other.id
        )

    def __hash__(
        self,
    ) -> int:
        return hash(self.id)

    def __repr__(
        self,
    ) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id})"
        )