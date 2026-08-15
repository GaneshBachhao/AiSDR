from enum import StrEnum


class LeadStatus(StrEnum):
    """
    Represents the lifecycle of an AI consulting lead.
    """

    NEW = "New"

    CONTACTED = "Contacted"

    QUALIFIED = "Qualified"

    DISQUALIFIED = "Disqualified"

    CONVERTED = "Converted"

    CLOSED = "Closed"