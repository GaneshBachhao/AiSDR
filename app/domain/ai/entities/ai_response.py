from datetime import UTC, datetime
from typing import Optional
from uuid import uuid4

from domain.shared.base import Entity

from ..enums.finish_reason import FinishReason
from ..exceptions.ai_exception import AIException
from ..value_objects.response_id import ResponseId
from ..value_objects.token_usage import TokenUsage


class AIResponse(Entity[ResponseId]):
    """
    Entity representing an AI completion.
    """

    def __init__(
        self,
        content: str,
        finish_reason: FinishReason,
        token_usage: TokenUsage,
        response_id: Optional[ResponseId] = None,
    ):
        content = content.strip()

        if not content:
            raise AIException(
                "Response content cannot be empty."
            )

        response_id = response_id or ResponseId(uuid4())

        super().__init__(response_id)

        self._content = content
        self._finish_reason = finish_reason
        self._token_usage = token_usage

        self._created_at = datetime.now(UTC)

    # --------------------------------------------------
    # Properties
    # --------------------------------------------------

    @property
    def content(self) -> str:
        return self._content

    @property
    def finish_reason(self) -> FinishReason:
        return self._finish_reason

    @property
    def token_usage(self) -> TokenUsage:
        return self._token_usage

    @property
    def created_at(self) -> datetime:
        return self._created_at