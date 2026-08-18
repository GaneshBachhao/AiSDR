from app.domain.shared.base import DomainEvent

from ..value_objects.ai_request_id import AIRequestId


class AIRequestCompleted(DomainEvent):
    """
    Raised when an AI request completes successfully.
    """

    def __init__(self, request_id: AIRequestId):
        super().__init__()
        self.request_id = request_id
