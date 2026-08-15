from .ai_exception import AIException


class InvalidAIRequestState(AIException):
    """
    Raised when an invalid AI request state transition is attempted.
    """

    pass