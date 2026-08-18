from enum import Enum


class WorkflowStatus(Enum):
    """
    Lifecycle states of a Workflow aggregate.
    """

    DRAFT = "DRAFT"

    READY = "READY"

    RUNNING = "RUNNING"

    PAUSED = "PAUSED"

    COMPLETED = "COMPLETED"

    FAILED = "FAILED"

    CANCELLED = "CANCELLED"
