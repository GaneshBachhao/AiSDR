"""
Update Contact application handler.

Architecture Freeze v5.0
"""

from __future__ import annotations

from sqlalchemy.exc import IntegrityError

from app.application.common.exceptions.conflict_exception import (
    ConflictException,
)
from app.application.common.exceptions.not_found_exception import (
    NotFoundException,
)
from app.application.common.exceptions.validation_exception import (
    ValidationException,
)
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.contact.contact_commands import UpdateContactCommand
from app.application.contact.contact_mapper import ContactMapper
from app.application.contact.contact_validator import ContactValidator
from app.application.contact.dto.contact_responses import ContactResponseDTO
from app.domain.contact.identifiers.contact_id import ContactId
from app.domain.contact.value_objects.email import Email


class UpdateContactHandler:
    """Handle the Update Contact use case."""

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        validator: ContactValidator,
        mapper: ContactMapper,
    ) -> None:
        self._unit_of_work = unit_of_work
        self._validator = validator
        self._mapper = mapper

    async def handle(
        self,
        command: UpdateContactCommand,
    ) -> ContactResponseDTO:
        """Validate, update, commit, and return a Contact."""
        validation = self._validator.validate_update(command)
        if not validation.is_valid:
            raise ValidationException(
                message="Contact validation failed.",
                details={error.field: error.message for error in validation.errors},
            )

        try:
            contact_id = ContactId(command.contact_id)
        except (TypeError, ValueError) as exc:
            raise ValidationException(
                message="Invalid contact id.",
                details={"contact_id": command.contact_id},
            ) from exc

        try:
            async with self._unit_of_work:
                contact = await self._unit_of_work.contact_repository.get_by_id(
                    contact_id,
                )

                if contact is None:
                    raise NotFoundException(
                        message="Contact not found.",
                        details={"contact_id": command.contact_id},
                    )

                if command.first_name is not None or command.last_name is not None:
                    contact.update_name(
                        first_name=(
                            command.first_name if command.first_name is not None else contact.first_name
                        ),
                        last_name=(command.last_name if command.last_name is not None else contact.last_name),
                    )

                if command.email is not None:
                    normalized_email = Email(command.email)

                    existing = await self._unit_of_work.contact_repository.find_by_email(
                        normalized_email.value,
                    )

                    if existing is not None and existing.id != contact.id:
                        raise ConflictException(
                            message="Contact already exists.",
                            details={"email": normalized_email.value},
                        )

                    contact.update_email(normalized_email)

                if command.phone is not None:
                    contact.update_phone(command.phone)

                if command.job_title is not None:
                    contact.update_job_title(command.job_title)

                if command.linkedin_url is not None:
                    contact.update_linkedin_url(command.linkedin_url)

                await self._unit_of_work.contact_repository.update(contact)

                # Explicit transaction boundary, consistent with Company.
                await self._unit_of_work.commit()

        except ValueError as exc:
            raise ValidationException(
                message="Contact validation failed.",
                details={"error": str(exc)},
            ) from exc
        except IntegrityError as exc:
            if "UNIQUE constraint failed: contacts.email" in str(exc):
                raise ConflictException(
                    message="Contact already exists.",
                    details={"email": command.email},
                ) from exc
            raise

        return self._mapper.to_response(contact)
