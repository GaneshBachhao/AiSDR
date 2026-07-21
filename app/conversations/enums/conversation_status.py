"""
Conversation Status

Represents the lifecycle of an email conversation.
"""

from enum import Enum


class ConversationStatus(str, Enum):
    """
    Conversation lifecycle.
    """

    OPEN = "OPEN"

    WAITING_FOR_REPLY = "WAITING_FOR_REPLY"

    RESPONDED = "RESPONDED"

    FOLLOW_UP_DUE = "FOLLOW_UP_DUE"

    MEETING_BOOKED = "MEETING_BOOKED"

    CLOSED = "CLOSED"

    LOST = "LOST"