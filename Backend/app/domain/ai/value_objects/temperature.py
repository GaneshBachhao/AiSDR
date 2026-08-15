from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Temperature:
    """
    Value object representing LLM temperature.
    """

    value: float = 0.7

    MIN = 0.0
    MAX = 2.0

    def __post_init__(self) -> None:

        if not self.MIN <= self.value <= self.MAX:
            raise ValueError(
                "Temperature must be between 0.0 and 2.0."
            )