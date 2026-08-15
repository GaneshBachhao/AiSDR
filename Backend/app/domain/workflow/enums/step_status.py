from enum import Enum


class StepStatus(Enum):
    """
    Lifecycle states of a Workflow Step.
    """

    PENDING = "PENDING"

    READY = "READY"

    RUNNING = "RUNNING"

    COMPLETED = "COMPLETED"

    FAILED = "FAILED"

    SKIPPED = "SKIPPED"