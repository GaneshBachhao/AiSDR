from enum import Enum


class JobStatus(str, Enum):
    """
    Represents the execution status of a background job.
    """

    PENDING = "PENDING"

    RUNNING = "RUNNING"

    COMPLETED = "COMPLETED"

    FAILED = "FAILED"