from enum import Enum


class ExecutionStatus(Enum):
    """
    Runtime execution lifecycle states.
    """

    CREATED = "CREATED"

    RUNNING = "RUNNING"

    COMPLETED = "COMPLETED"

    FAILED = "FAILED"

    CANCELLED = "CANCELLED"