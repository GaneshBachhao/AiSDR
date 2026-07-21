from domain.shared.base import DomainEvent

from ..value_objects.ai_request_id import AIRequestId


class AIRequestStarted(DomainEvent):
    """
    Raised when AI execution begins.
    """

    def __init__(self, request_id: AIRequestId):
        super().__init__()
        self.request_id = request_id