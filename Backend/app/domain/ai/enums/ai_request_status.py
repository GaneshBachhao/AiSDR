from enum import Enum


class AIRequestStatus(str, Enum):
    """
    Represents the lifecycle of an AI request.
    """

    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"