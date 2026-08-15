from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.ai.enums.finish_reason import FinishReason
from app.domain.ai.value_objects.response_id import ResponseId
from app.domain.ai.value_objects.token_usage import TokenUsage


@dataclass(eq=False)
class AIResponse:
    """
    Entity representing an AI completion.
    """

    id: ResponseId = field(
        default_factory=ResponseId,
        kw_only=True,
    )

    content: str = ""

    finish_reason: FinishReason = FinishReason.STOP

    token_usage: TokenUsage = field(
        default_factory=TokenUsage,
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    def __post_init__(self) -> None:

        self.content = self.content.strip()

        if not self.content:
            raise ValueError(
                "AI response cannot be empty."
            )