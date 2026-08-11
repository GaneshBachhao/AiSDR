"""Lead application queries."""

from __future__ import annotations

from dataclasses import dataclass

from app.application.common.queries.query import Query


@dataclass(frozen=True)
class GetLeadQuery(Query):
    """Retrieve a Lead by ID."""

    lead_id: str


@dataclass(frozen=True)
class ListLeadQuery(Query):
    """List Leads with optional relationship filters."""

    company_id: str | None = None
    contact_id: str | None = None
    skip: int = 0
    limit: int = 100


@dataclass(frozen=True)
class SearchLeadQuery(Query):
    """Search Leads."""

    search_term: str
    company_id: str | None = None
    contact_id: str | None = None
    skip: int = 0
    limit: int = 100
