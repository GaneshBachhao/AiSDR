"""Check Suppression application handler."""

from __future__ import annotations

from app.application.common.exceptions.validation_exception import ValidationException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.suppression.dto.suppression_responses import (
    SuppressionCheckResponseDTO,
)
from app.application.suppression.suppression_mapper import SuppressionMapper
from app.domain.contact.value_objects.email import Email


class CheckSuppressionHandler:
    """Check whether a single email address is currently suppressed.

    This is the check a real send path (EPIC-09, not yet built) would
    call before contacting anyone -- see suppression_repository.find_by_email.
    """

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, email: str) -> SuppressionCheckResponseDTO:
        try:
            normalized = Email(email)
        except ValueError as exc:
            raise ValidationException(
                message="Suppression check validation failed.",
                details={"error": str(exc)},
            ) from exc

        async with self._unit_of_work:
            entry = await self._unit_of_work.suppression_repository.find_by_email(normalized.value)

        return SuppressionCheckResponseDTO(
            email=normalized.value,
            suppressed=entry is not None,
            entry=(SuppressionMapper.to_response(entry) if entry is not None else None),
        )
