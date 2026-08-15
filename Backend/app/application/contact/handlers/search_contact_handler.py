"""
Search Contacts application handler.

Architecture Freeze v5.0
"""

from __future__ import annotations

from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.contact.contact_mapper import ContactMapper
from app.application.contact.contact_queries import SearchContactsQuery
from app.application.contact.dto.contact_responses import ContactResponseDTO


class SearchContactHandler:
    """Handle the Search Contacts use case."""

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        mapper: ContactMapper,
    ) -> None:
        self._unit_of_work = unit_of_work
        self._mapper = mapper

    async def handle(
        self,
        query: SearchContactsQuery,
    ) -> list[ContactResponseDTO]:
        """Search Contacts and return response DTOs."""
        async with self._unit_of_work:
            contacts = await self._unit_of_work.contact_repository.search(
                search_text=query.search_text,
                skip=query.skip,
                limit=query.limit,
            )

        return self._mapper.to_response_list(contacts)
