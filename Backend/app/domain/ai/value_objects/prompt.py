from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Prompt:
    """
    Value object representing an AI prompt.
    """

    value: str

    MIN_LENGTH = 1
    MAX_LENGTH = 50000

    def __post_init__(self) -> None:

        value = self.value.strip()

        if len(value) < self.MIN_LENGTH:
            raise ValueError("Prompt cannot be empty.")

        if len(value) > self.MAX_LENGTH:
            raise ValueError("Prompt exceeds maximum length.")

        object.__setattr__(
            self,
            "value",
            value,
        )

    def __str__(self) -> str:
        return self.value
