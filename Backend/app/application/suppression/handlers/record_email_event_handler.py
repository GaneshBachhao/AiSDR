"""Record Email Event application handler (EPIC-11, bounce/complaint webhook)."""

from __future__ import annotations

from app.application.common.exceptions.validation_exception import ValidationException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.suppression.dto.suppression_responses import (
    SuppressionEntryResponseDTO,
)
from app.application.suppression.suppression_commands import RecordEmailEventCommand
from app.application.suppression.suppression_mapper import SuppressionMapper
from app.domain.contact.value_objects.email import Email
from app.domain.suppression.entities.suppression_entry import SuppressionEntry
from app.domain.suppression.enums.suppression_reason import SuppressionReason

_EVENT_TYPE_TO_REASON = {
    "bounce": SuppressionReason.BOUNCE,
    "complaint": SuppressionReason.COMPLAINT,
}


class RecordEmailEventHandler:
    """Auto-suppress an email address on a bounce/complaint event.

    Idempotent: an event for an already-suppressed email is a no-op --
    it doesn't overwrite the original reason/notes.
    """

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, command: RecordEmailEventCommand) -> SuppressionEntryResponseDTO:
        try:
            email = Email(command.email)
        except ValueError as exc:
            raise ValidationException(
                message="Email event validation failed.",
                details={"error": str(exc)},
            ) from exc

        reason = _EVENT_TYPE_TO_REASON.get(command.event_type.strip().lower())
        if reason is None:
            raise ValidationException(
                message="Email event validation failed.",
                details={"error": f"Unknown event_type '{command.event_type}'."},
            )

        async with self._unit_of_work:
            existing = await self._unit_of_work.suppression_repository.find_by_email(email.value)
            if existing is not None:
                return SuppressionMapper.to_response(existing)

            entry = SuppressionEntry(email=email, reason=reason, notes=command.reason)
            await self._unit_of_work.suppression_repository.add(entry)
            await self._unit_of_work.commit()

        return SuppressionMapper.to_response(entry)
