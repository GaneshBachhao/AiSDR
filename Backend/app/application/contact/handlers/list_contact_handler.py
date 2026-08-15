"""
List Contacts application handler.

Architecture Freeze v5.0
"""

from __future__ import annotations

from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.contact.contact_mapper import ContactMapper
from app.application.contact.contact_queries import ListContactsQuery
from app.application.contact.dto.contact_responses import ContactResponseDTO


class ListContactHandler:
    """Handle the List Contacts use case."""

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        mapper: ContactMapper,
    ) -> None:
        self._unit_of_work = unit_of_work
        self._mapper = mapper

    async def handle(
        self,
        query: ListContactsQuery,
    ) -> list[ContactResponseDTO]:
        """Retrieve paginated Contacts."""
        async with self._unit_of_work:
            contacts = await self._unit_of_work.contact_repository.list(
                skip=query.skip,
                limit=query.limit,
            )

        return self._mapper.to_response_list(contacts)
