from enum import StrEnum


class DiscoveryStatus(StrEnum):
    """
    Represents the lifecycle of a discovery session.
    """

    CREATED = "Created"

    IN_PROGRESS = "In Progress"

    ON_HOLD = "On Hold"

    COMPLETED = "Completed"

    CANCELLED = "Cancelled"