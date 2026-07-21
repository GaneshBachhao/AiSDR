from enum import StrEnum


class ImplementationStatus(StrEnum):
    """
    Represents the execution status of a roadmap phase.
    """

    PLANNED = "Planned"

    IN_PROGRESS = "In Progress"

    COMPLETED = "Completed"

    BLOCKED = "Blocked"