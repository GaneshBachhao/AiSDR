"""
Delete Contact application handler.

Architecture Freeze v5.0
"""

from __future__ import annotations

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.exceptions.validation_exception import ValidationException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.contact.contact_commands import DeleteContactCommand
from app.domain.contact.identifiers.contact_id import ContactId


class DeleteContactHandler:
    """Handles the Delete Contact use case."""

    def __init__(
        self,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._unit_of_work = unit_of_work

    async def handle(
        self,
        command: DeleteContactCommand,
    ) -> None:
        """Delete a Contact and commit the transaction."""
        try:
            contact_id = ContactId(command.contact_id)
        except (TypeError, ValueError) as exc:
            raise ValidationException(
                message="Invalid contact id.",
                details={"contact_id": command.contact_id},
            ) from exc

        async with self._unit_of_work:
            contact = await self._unit_of_work.contact_repository.get_by_id(
                contact_id,
            )

            if contact is None:
                raise NotFoundException(
                    message="Contact not found.",
                    details={"contact_id": command.contact_id},
                )

            # Repository.delete expects the typed identifier, not the entity.
            await self._unit_of_work.contact_repository.delete(contact_id)

            # Explicit transaction boundary.
            await self._unit_of_work.commit()
