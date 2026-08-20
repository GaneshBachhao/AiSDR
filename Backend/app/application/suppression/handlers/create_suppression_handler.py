"""Create Suppression application handler."""

from __future__ import annotations

from app.application.common.exceptions.validation_exception import ValidationException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.suppression.dto.suppression_responses import (
    SuppressionEntryResponseDTO,
)
from app.application.suppression.suppression_commands import CreateSuppressionCommand
from app.application.suppression.suppression_mapper import SuppressionMapper
from app.domain.contact.value_objects.email import Email


class CreateSuppressionHandler:
    """Add an email to the do-not-contact list.

    Idempotent: suppressing an already-suppressed email returns the
    existing record rather than erroring -- re-suppressing isn't a
    conflict the way a duplicate Company name is, it's a no-op-success.
    """

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, command: CreateSuppressionCommand) -> SuppressionEntryResponseDTO:
        try:
            email = Email(command.email)
        except ValueError as exc:
            raise ValidationException(
                message="Suppression validation failed.",
                details={"error": str(exc)},
            ) from exc

        async with self._unit_of_work:
            existing = await self._unit_of_work.suppression_repository.find_by_email(email.value)
            if existing is not None:
                return SuppressionMapper.to_response(existing)

            entry = SuppressionMapper.to_domain(command)
            await self._unit_of_work.suppression_repository.add(entry)
            await self._unit_of_work.commit()

        return SuppressionMapper.to_response(entry)
