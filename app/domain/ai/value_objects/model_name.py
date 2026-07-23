from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelName:
    """
    Value object representing an AI model name.
    """

    value: str

    MIN_LENGTH = 2
    MAX_LENGTH = 100

    def __post_init__(self) -> None:

        value = self.value.strip()

        if len(value) < self.MIN_LENGTH:
            raise ValueError(
                "Model name is too short."
            )

        if len(value) > self.MAX_LENGTH:
            raise ValueError(
                "Model name is too long."
            )

        object.__setattr__(
            self,
            "value",
            value,
        )

    def __str__(self) -> str:
        return self.value