from app.domain.shared.base import DomainEvent

from ..value_objects.ai_request_id import AIRequestId
from ..value_objects.response_id import ResponseId


class AIResponseReceived(DomainEvent):
    """
    Raised when an AI response is received.
    """

    def __init__(
        self,
        request_id: AIRequestId,
        response_id: ResponseId,
    ):
        super().__init__()
        self.request_id = request_id
        self.response_id = response_id