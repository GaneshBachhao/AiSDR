from enum import Enum


class AIRequestStatus(Enum):
    """
    Lifecycle states of an AI request.
    """

    PENDING = "PENDING"

    RUNNING = "RUNNING"

    COMPLETED = "COMPLETED"

    FAILED = "FAILED"

    CANCELLED = "CANCELLED"