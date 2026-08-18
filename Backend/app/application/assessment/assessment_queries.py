"""
Assessment queries.
"""

from __future__ import annotations

from app.application.common.queries.query import (
    Query,
)


class GetAssessmentQuery(Query):
    """
    Query to retrieve an assessment by its identifier.
    """

    assessment_id: str


class ListAssessmentsQuery(Query):
    """
    Query to retrieve assessments.
    """

    page: int = 1

    page_size: int = 10

    discovery_id: str | None = None
