"""
Email Direction Enum
"""

from enum import Enum


class EmailDirection(str, Enum):
    """
    Direction of an email.
    """

    OUTBOUND = "OUTBOUND"

    INBOUND = "INBOUND"