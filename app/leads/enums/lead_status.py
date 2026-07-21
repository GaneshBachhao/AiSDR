"""
Lead Status

Represents the business lifecycle
of a lead.
"""

from enum import Enum


class LeadStatus(str, Enum):
    """
    Lead lifecycle.
    """

    NEW = "NEW"

    DISCOVERED = "DISCOVERED"

    QUALIFIED = "QUALIFIED"

    CONTACTED = "CONTACTED"

    MEETING_SCHEDULED = "MEETING_SCHEDULED"

    PROPOSAL_SENT = "PROPOSAL_SENT"

    NEGOTIATION = "NEGOTIATION"

    WON = "WON"

    LOST = "LOST"

    ARCHIVED = "ARCHIVED"