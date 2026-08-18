"""
Contact Application Mapper.

Architecture Freeze v5.0

Maps application request DTOs/commands to the Contact domain
and maps the Contact domain to application response DTOs.
"""

from __future__ import annotations

from app.application.contact.contact_commands import (
    CreateContactCommand,
    UpdateContactCommand,
)
from app.application.contact.dto.contact_requests import (
    CreateContactRequestDTO,
    UpdateContactRequestDTO,
)
from app.application.contact.dto.contact_responses import (
    ContactResponseDTO,
)
from app.domain.company.identifiers.company_id import (
    CompanyId,
)
from app.domain.contact.entities.contact import (
    Contact,
)
from app.domain.contact.identifiers.contact_id import (
    ContactId,
)
from app.domain.contact.value_objects.email import (
    Email,
)


class ContactMapper:
    """Application mapper for the Contact aggregate."""

    @staticmethod
    def to_create_command(
        request: CreateContactRequestDTO,
    ) -> CreateContactCommand:
        """Map a create request DTO to a create command."""
        return CreateContactCommand(
            company_id=request.company_id,
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            phone=request.phone,
            job_title=request.job_title,
            linkedin_url=request.linkedin_url,
        )

    @staticmethod
    def to_update_command(
        request: UpdateContactRequestDTO,
        contact_id: str,
    ) -> UpdateContactCommand:
        """Map an update request DTO plus route id to an update command."""
        return UpdateContactCommand(
            contact_id=contact_id,
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            phone=request.phone,
            job_title=request.job_title,
            linkedin_url=request.linkedin_url,
        )

    @staticmethod
    def to_domain(
        command: CreateContactCommand,
    ) -> Contact:
        """Map a create command to a Contact domain aggregate."""
        return Contact(
            id=ContactId(),
            company_id=CompanyId(command.company_id),
            first_name=command.first_name,
            last_name=command.last_name,
            email=Email(command.email),
            phone=command.phone,
            job_title=command.job_title,
            linkedin_url=command.linkedin_url,
        )

    @staticmethod
    def to_response(
        contact: Contact,
    ) -> ContactResponseDTO:
        """Map a Contact domain aggregate to a response DTO."""
        return ContactResponseDTO(
            id=str(contact.id),
            company_id=str(contact.company_id),
            first_name=contact.first_name,
            last_name=contact.last_name,
            email=contact.email.value,
            phone=contact.phone,
            job_title=contact.job_title,
            linkedin_url=contact.linkedin_url,
            is_active=contact.is_active,
        )

    @staticmethod
    def to_response_list(
        contacts: list[Contact],
    ) -> list[ContactResponseDTO]:
        """Map a Contact collection to response DTOs."""
        return [ContactMapper.to_response(contact) for contact in contacts]
