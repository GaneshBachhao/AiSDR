from enum import StrEnum


class ImplementationPriority(StrEnum):
    """
    Represents the implementation priority of a solution.
    """

    LOW = "Low"

    MEDIUM = "Medium"

    HIGH = "High"

    CRITICAL = "Critical"