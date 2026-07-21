"""
Contact Source Enum

Indicates how the contact
was discovered.
"""

from enum import Enum


class ContactSource(str, Enum):
    """
    Contact origin.
    """

    MANUAL = "MANUAL"

    WEBSITE = "WEBSITE"

    LINKEDIN = "LINKEDIN"

    APOLLO = "APOLLO"

    HUNTER = "HUNTER"

    CLEARBIT = "CLEARBIT"

    AI_DISCOVERY = "AI_DISCOVERY"

    CSV_IMPORT = "CSV_IMPORT"