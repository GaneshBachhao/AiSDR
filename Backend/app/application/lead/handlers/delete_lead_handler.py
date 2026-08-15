"""
Delete Lead application handler.

Architecture Freeze v5.0
"""

from __future__ import annotations

from app.application.common.exceptions.not_found_exception import (
    NotFoundException,
)
from app.application.common.exceptions.validation_exception import (
    ValidationException,
)
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.lead.lead_commands import DeleteLeadCommand
from app.domain.lead.identifiers.lead_id import LeadId


class DeleteLeadHandler:
    """Handle the Delete Lead use case."""

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, command: DeleteLeadCommand) -> None:
        try:
            lead_id = LeadId(command.lead_id)
        except (TypeError, ValueError) as exc:
            raise ValidationException(
                message="Invalid lead id.",
                details={"lead_id": command.lead_id},
            ) from exc

        async with self._unit_of_work:
            lead = await self._unit_of_work.lead_repository.get_by_id(
                lead_id,
            )

            if lead is None:
                raise NotFoundException(
                    message="Lead not found.",
                    details={"lead_id": command.lead_id},
                )

            await self._unit_of_work.lead_repository.delete(lead.id)
            await self._unit_of_work.commit()
