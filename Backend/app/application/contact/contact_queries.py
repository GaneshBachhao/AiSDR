"""
Contact Queries.

Contains all query objects related to Contact aggregate.

Architecture Freeze v4.0
- Queries live at aggregate application root.
- Queries carry request/filter data only.
- Query handlers execute repository operations.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.common.queries.query import (
    Query,
)


@dataclass(frozen=True, slots=True)
class GetContactQuery(Query):
    """
    Query to retrieve a contact by id.
    """

    contact_id: str


@dataclass(frozen=True, slots=True)
class ListContactsQuery(Query):
    """
    Query to list contacts.

    Supports future pagination.
    """

    skip: int = 0

    limit: int = 100


@dataclass(frozen=True, slots=True)
class SearchContactsQuery(Query):
    """
    Query to search contacts.
    """

    search_text: str

    skip: int = 0

    limit: int = 100