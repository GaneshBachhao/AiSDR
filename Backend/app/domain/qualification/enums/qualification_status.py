"""
Qualification status enumeration.
"""

from __future__ import annotations

from enum import Enum


class QualificationStatus(
    str,
    Enum,
):
    """
    Qualification lifecycle status.
    """

    QUALIFIED = "Qualified"

    PARTIALLY_QUALIFIED = "Partially Qualified"

    NEEDS_NURTURING = "Needs Nurturing"

    DISQUALIFIED = "Disqualified"