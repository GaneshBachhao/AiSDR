"""
Discovery identifier value object.

Provides strongly typed identity for Discovery entities.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True)
class DiscoveryId:
    """
    Strongly typed discovery identifier.
    """

    value: UUID

    @classmethod
    def create(cls) -> "DiscoveryId":
        """
        Creates a new discovery identifier.
        """
        return cls(uuid4())

    @classmethod
    def from_value(
        cls,
        value: UUID | str,
    ) -> "DiscoveryId":
        """
        Creates identifier from existing value.
        """

        if isinstance(value, str):
            value = UUID(value)

        return cls(value)

    def __str__(self) -> str:
        return str(self.value)