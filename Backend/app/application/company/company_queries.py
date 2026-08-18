"""
Company Queries.

Architecture Freeze v5.0
Queries contain request/filter data only. Query handlers execute repository operations.
"""

from __future__ import annotations

from app.application.common.queries.query import Query


class GetCompanyQuery(Query):
    """Query to fetch a company by id."""

    company_id: str


class ListCompaniesQuery(Query):
    """Query to list companies with pagination."""

    skip: int = 0
    limit: int = 100


class SearchCompaniesQuery(Query):
    """Query to search companies with pagination."""

    search_text: str
    skip: int = 0
    limit: int = 100
