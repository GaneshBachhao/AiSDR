"""
Update Lead application handler.

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
from app.application.lead.dto.lead_responses import LeadResponseDTO
from app.application.lead.lead_commands import UpdateLeadCommand
from app.application.lead.lead_mapper import LeadMapper
from app.application.lead.lead_validator import LeadValidator
from app.domain.contact.identifiers.contact_id import ContactId
from app.domain.lead.identifiers.lead_id import LeadId


class UpdateLeadHandler:
    """Handle the Update Lead use case."""

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(
        self,
        command: UpdateLeadCommand,
    ) -> LeadResponseDTO:
        try:
            LeadValidator.validate_update(command)
            lead_id = LeadId(command.lead_id)
        except (TypeError, ValueError) as exc:
            raise ValidationException(
                message="Lead validation failed.",
                details={"error": str(exc)},
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

            if command.contact_id is not None:
                contact = await self._unit_of_work.contact_repository.get_by_id(
                    ContactId(command.contact_id),
                )

                if contact is None:
                    raise NotFoundException(
                        message="Contact not found.",
                        details={"contact_id": command.contact_id},
                    )

                if contact.company_id != lead.company_id:
                    raise ValidationException(
                        message="Contact does not belong to the Lead company.",
                        details={
                            "company_id": str(lead.company_id),
                            "contact_id": command.contact_id,
                        },
                    )

            try:
                LeadMapper.apply_update(lead, command)
            except (TypeError, ValueError) as exc:
                raise ValidationException(
                    message="Lead update failed.",
                    details={"error": str(exc)},
                ) from exc

            await self._unit_of_work.lead_repository.update(lead)
            await self._unit_of_work.commit()

        return LeadMapper.to_response(lead)
