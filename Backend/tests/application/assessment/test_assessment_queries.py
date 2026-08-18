"""
Tests for Assessment queries.
"""

from __future__ import annotations

from app.application.assessment.assessment_queries import (
    GetAssessmentQuery,
    ListAssessmentsQuery,
)


class TestGetAssessmentQuery:
    """
    Tests for GetAssessmentQuery.
    """

    def test_get_assessment_query(self) -> None:
        query = GetAssessmentQuery(
            assessment_id="assessment-123",
        )

        assert query.assessment_id == "assessment-123"


class TestListAssessmentsQuery:
    """
    Tests for ListAssessmentsQuery.
    """

    def test_list_assessments_query_defaults(self) -> None:
        query = ListAssessmentsQuery()

        assert query.page == 1
        assert query.page_size == 10
        assert query.discovery_id is None

    def test_list_assessments_query_with_filters(self) -> None:
        query = ListAssessmentsQuery(
            page=2,
            page_size=25,
            discovery_id="discovery-123",
        )

        assert query.page == 2
        assert query.page_size == 25
        assert query.discovery_id == "discovery-123"
