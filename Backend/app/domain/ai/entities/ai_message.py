from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.ai.enums.message_role import MessageRole
from app.domain.ai.value_objects.message_id import MessageId


@dataclass(eq=False)
class AIMessage:
    """
    Entity representing a message exchanged
    during an AI conversation.
    """

    id: MessageId = field(
        default_factory=MessageId,
        kw_only=True,
    )

    role: MessageRole = MessageRole.USER

    content: str = ""

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    def __post_init__(self) -> None:

        self.content = self.content.strip()

        if not self.content:
            raise ValueError("Message content cannot be empty.")
