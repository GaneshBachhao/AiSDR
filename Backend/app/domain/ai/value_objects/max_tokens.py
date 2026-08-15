from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MaxTokens:
    """
    Value object representing the maximum number of tokens.
    """

    value: int = 1024

    MIN = 1
    MAX = 32768

    def __post_init__(self) -> None:

        if not self.MIN <= self.value <= self.MAX:
            raise ValueError(
                "Max tokens out of allowed range."
            )