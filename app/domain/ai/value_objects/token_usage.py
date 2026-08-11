from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TokenUsage:
    """
    Represents token consumption for an AI request.
    """

    prompt_tokens: int = 0

    completion_tokens: int = 0

    total_tokens: int = 0

    def __post_init__(self) -> None:

        if self.prompt_tokens < 0:
            raise ValueError(
                "Prompt tokens cannot be negative."
            )

        if self.completion_tokens < 0:
            raise ValueError(
                "Completion tokens cannot be negative."
            )

        if self.total_tokens < 0:
            raise ValueError(
                "Total tokens cannot be negative."
            )

        calculated = (
            self.prompt_tokens
            + self.completion_tokens
        )

        if self.total_tokens == 0:
            object.__setattr__(
                self,
                "total_tokens",
                calculated,
            )

        elif self.total_tokens != calculated:
            raise ValueError(
                "Total tokens must equal prompt + completion tokens."
            )