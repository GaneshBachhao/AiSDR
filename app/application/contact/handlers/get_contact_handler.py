"""
Get Contact application handler.

Architecture Freeze v5.0
"""

from __future__ import annotations

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.exceptions.validation_exception import ValidationException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.contact.contact_mapper import ContactMapper
from app.application.contact.contact_queries import GetContactQuery
from app.application.contact.dto.contact_responses import ContactResponseDTO
from app.domain.contact.identifiers.contact_id import ContactId


class GetContactHandler:
    """Handle the Get Contact use case."""

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        mapper: ContactMapper,
    ) -> None:
        self._unit_of_work = unit_of_work
        self._mapper = mapper

    async def handle(
        self,
        query: GetContactQuery,
    ) -> ContactResponseDTO:
        """Retrieve a Contact by id."""
        try:
            contact_id = ContactId(query.contact_id)
        except (TypeError, ValueError) as exc:
            raise ValidationException(
                message="Invalid contact id.",
                details={"contact_id": query.contact_id},
            ) from exc

        async with self._unit_of_work:
            contact = await self._unit_of_work.contact_repository.get_by_id(
                contact_id,
            )

            if contact is None:
                raise NotFoundException(
                    message="Contact not found.",
                    details={"contact_id": query.contact_id},
                )

        return self._mapper.to_response(contact)
