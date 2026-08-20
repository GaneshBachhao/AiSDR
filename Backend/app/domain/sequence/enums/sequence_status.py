from enum import StrEnum


class SequenceStatus(StrEnum):
    """
    Lifecycle status of a Sequence.
    """

    DRAFT = "Draft"

    ACTIVE = "Active"

    COMPLETED = "Completed"

    STOPPED = "Stopped"
