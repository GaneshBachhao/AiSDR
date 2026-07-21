from datetime import UTC, datetime
from typing import Optional
from uuid import uuid4

from domain.shared.base import Entity

from ..enums.message_role import MessageRole
from ..exceptions.ai_exception import AIException
from ..value_objects.message_id import MessageId


class AIMessage(Entity[MessageId]):
    """
    Entity representing a conversation message.
    """

    def __init__(
        self,
        role: MessageRole,
        content: str,
        sequence: int,
        message_id: Optional[MessageId] = None,
    ):
        content = content.strip()

        if not content:
            raise AIException(
                "Message content cannot be empty."
            )

        if sequence < 1:
            raise AIException(
                "Message sequence must be greater than zero."
            )

        message_id = message_id or MessageId(uuid4())

        super().__init__(message_id)

        self._role = role
        self._content = content
        self._sequence = sequence

        self._created_at = datetime.now(UTC)

    # --------------------------------------------------
    # Properties
    # --------------------------------------------------

    @property
    def role(self) -> MessageRole:
        return self._role

    @property
    def content(self) -> str:
        return self._content

    @property
    def sequence(self) -> int:
        return self._sequence

    @property
    def created_at(self) -> datetime:
        return self._created_at