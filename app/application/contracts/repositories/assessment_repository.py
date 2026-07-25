"""
Assessment repository contract.
"""

from __future__ import annotations

from app.application.common.interfaces.repository import (
    Repository,
)
from app.domain.assessment.entities.assessment import Assessment
from app.domain.assessment.identifiers.assessment_id import AssessmentId


class AssessmentRepository(
    Repository[Assessment, AssessmentId],
):
    """
    Assessment persistence contract.
    """

    pass