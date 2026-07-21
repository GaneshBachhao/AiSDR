"""
Automation Priority
"""

from enum import Enum


class AutomationPriority(str, Enum):
    """
    Priority assigned to automation actions.
    """

    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"

    CRITICAL = "CRITICAL"