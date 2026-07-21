"""
Email Status Enum
"""

from enum import Enum


class EmailStatus(str, Enum):
    """
    Lifecycle status of an email.
    """

    DRAFT = "DRAFT"

    QUEUED = "QUEUED"

    SENDING = "SENDING"

    SENT = "SENT"

    DELIVERED = "DELIVERED"

    OPENED = "OPENED"

    CLICKED = "CLICKED"

    REPLIED = "REPLIED"

    BOUNCED = "BOUNCED"

    FAILED = "FAILED"

    CANCELLED = "CANCELLED"