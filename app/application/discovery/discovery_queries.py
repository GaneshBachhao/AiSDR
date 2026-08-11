"""
Discovery application queries.

Architecture Freeze v5.0
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.common.queries.query import Query


@dataclass(frozen=True, slots=True)
class GetDiscoveryQuery(Query):
    """Query to retrieve a discovery by id."""

    discovery_id: str


@dataclass(frozen=True, slots=True)
class ListDiscoveryQuery(Query):
    """Query to list discoveries with pagination."""

    skip: int = 0
    limit: int = 100


@dataclass(frozen=True, slots=True)
class SearchDiscoveryQuery(Query):
    """Query to search discoveries."""

    search_text: str
    skip: int = 0
    limit: int = 100
