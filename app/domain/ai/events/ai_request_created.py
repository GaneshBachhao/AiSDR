from domain.shared.base import DomainEvent

from ..value_objects.ai_request_id import AIRequestId


class AIRequestCreated(DomainEvent):
    """
    Raised when a new AI request is created.
    """

    def __init__(self, request_id: AIRequestId):
        super().__init__()
        self.request_id = request_id