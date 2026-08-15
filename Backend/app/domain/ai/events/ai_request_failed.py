from app.domain.shared.base import DomainEvent

from ..value_objects.ai_request_id import AIRequestId


class AIRequestFailed(DomainEvent):
    """
    Raised when an AI request fails.
    """

    def __init__(
        self,
        request_id: AIRequestId,
        reason: str,
    ):
        super().__init__()
        self.request_id = request_id
        self.reason = reason