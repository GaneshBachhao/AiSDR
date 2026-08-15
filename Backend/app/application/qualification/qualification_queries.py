"""
Qualification queries.
"""

from __future__ import annotations

from app.application.common.queries.query import (
    Query,
)


class GetQualificationQuery(Query):
    """
    Query to retrieve a qualification by identifier.
    """

    qualification_id: str


class ListQualificationsQuery(Query):
    """
    Query to retrieve qualifications.
    """

    page: int = 1

    page_size: int = 10

    lead_id: str | None = None

    assessment_id: str | None = None