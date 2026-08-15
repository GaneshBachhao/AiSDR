from __future__ import annotations

from abc import ABC


class ValueObject(ABC):
    """
    Base class for all domain value objects.

    Value objects are immutable and compared by their values,
    not by identity.
    """

    def __eq__(
        self,
        other: object,
    ) -> bool:
        """
        Compare value objects by their attributes.
        """
        return (
            isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__
        )

    def __hash__(self) -> int:
        """
        Generate hash from value attributes.
        """
        return hash(
            tuple(
                sorted(
                    self.__dict__.items()
                )
            )
        )

    def __repr__(self) -> str:
        """
        Return readable representation.
        """
        values = ", ".join(
            f"{key}={value!r}"
            for key, value in self.__dict__.items()
        )

        return (
            f"{self.__class__.__name__}"
            f"({values})"
        )