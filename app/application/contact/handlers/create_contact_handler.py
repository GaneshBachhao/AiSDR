"""
Create Contact application handler.

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
from app.application.common.interfaces.unit_of_work import (
    UnitOfWork,
)
from app.application.contact.contact_commands import (
    CreateContactCommand,
)
from app.application.contact.contact_mapper import (
    ContactMapper,
)
from app.application.contact.contact_validator import (
    ContactValidator,
)
from app.application.contact.dto.contact_responses import (
    ContactResponseDTO,
)
from app.domain.company.identifiers.company_id import (
    CompanyId,
)


class CreateContactHandler:
    """Handle the Create Contact use case."""

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
        command: CreateContactCommand,
    ) -> ContactResponseDTO:
        """Validate, create, persist, commit, and return a Contact."""
        validation = self._validator.validate_create(command)
        if not validation.is_valid:
            raise ValidationException(
                message="Contact validation failed.",
                details={
                    error.field: error.message
                    for error in validation.errors
                },
            )

        try:
            company_id = CompanyId(command.company_id)
            contact = self._mapper.to_domain(command)
        except (TypeError, ValueError) as exc:
            raise ValidationException(
                message="Contact validation failed.",
                details={"error": str(exc)},
            ) from exc

        try:
            async with self._unit_of_work:
                company = await self._unit_of_work.company_repository.get_by_id(
                    company_id,
                )

                if company is None:
                    raise NotFoundException(
                        message="Company not found.",
                        details={"company_id": command.company_id},
                    )

                existing = (
                    await self._unit_of_work.contact_repository.find_by_email(
                        contact.email.value,
                    )
                )

                if existing is not None:
                    raise ConflictException(
                        message="Contact already exists.",
                        details={"email": contact.email.value},
                    )

                await self._unit_of_work.contact_repository.add(contact)

                # Explicit transaction boundary, consistent with Company.
                await self._unit_of_work.commit()

        except IntegrityError as exc:
            if "UNIQUE constraint failed: contacts.email" in str(exc):
                raise ConflictException(
                    message="Contact already exists.",
                    details={"email": contact.email.value},
                ) from exc
            raise

        return self._mapper.to_response(contact)
