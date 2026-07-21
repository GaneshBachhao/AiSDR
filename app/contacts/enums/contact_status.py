"""
Contact Status Enum

Represents the lifecycle state of a contact.
"""

from enum import Enum


class ContactStatus(str, Enum):
    """
    Contact lifecycle status.
    """

    ACTIVE = "ACTIVE"

    UNKNOWN = "UNKNOWN"

    INVALID = "INVALID"

    BOUNCED = "BOUNCED"

    UNSUBSCRIBED = "UNSUBSCRIBED"