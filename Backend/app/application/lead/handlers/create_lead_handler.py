"""
Create Lead application handler.

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
from app.application.lead.lead_commands import CreateLeadCommand
from app.application.lead.lead_mapper import LeadMapper
from app.application.lead.lead_validator import LeadValidator
from app.domain.company.identifiers.company_id import CompanyId
from app.domain.contact.identifiers.contact_id import ContactId


class CreateLeadHandler:
    """Handle the Create Lead use case."""

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(
        self,
        command: CreateLeadCommand,
    ) -> LeadResponseDTO:
        """Validate, verify relationships, persist, commit, and return."""
        try:
            LeadValidator.validate_create(command)
            company_id = CompanyId(command.company_id)
            contact_id = ContactId(command.contact_id)
            lead = LeadMapper.to_domain(command)
        except (TypeError, ValueError) as exc:
            raise ValidationException(
                message="Lead validation failed.",
                details={"error": str(exc)},
            ) from exc

        async with self._unit_of_work:
            company = await self._unit_of_work.company_repository.get_by_id(
                company_id,
            )
            if company is None:
                raise NotFoundException(
                    message="Company not found.",
                    details={"company_id": command.company_id},
                )

            contact = await self._unit_of_work.contact_repository.get_by_id(
                contact_id,
            )
            if contact is None:
                raise NotFoundException(
                    message="Contact not found.",
                    details={"contact_id": command.contact_id},
                )

            if contact.company_id != company.id:
                raise ValidationException(
                    message="Contact does not belong to the specified company.",
                    details={
                        "company_id": command.company_id,
                        "contact_id": command.contact_id,
                    },
                )

            await self._unit_of_work.lead_repository.add(lead)
            await self._unit_of_work.commit()

        return LeadMapper.to_response(lead)
