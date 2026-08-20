"""
Lead Application Mapper.

Architecture Freeze v5.0
Maps:
- Request DTO -> Command
- Command -> Domain Entity
- Domain Entity -> Response DTO
"""

from __future__ import annotations

from app.application.lead.dto.lead_requests import (
    CreateLeadRequestDTO,
    UpdateLeadRequestDTO,
)
from app.application.lead.dto.lead_responses import LeadResponseDTO
from app.application.lead.lead_commands import (
    CreateLeadCommand,
    UpdateLeadCommand,
)
from app.domain.company.identifiers.company_id import CompanyId
from app.domain.contact.identifiers.contact_id import ContactId
from app.domain.lead.entities.lead import Lead
from app.domain.lead.enums.lead_source import LeadSource
from app.domain.lead.enums.lead_status import LeadStatus
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.lead.value_objects.lead_score import LeadScore


class LeadMapper:
    """Maps Lead application and domain objects."""

    @staticmethod
    def to_create_command(
        request: CreateLeadRequestDTO,
    ) -> CreateLeadCommand:
        """Map create request DTO to command."""
        return CreateLeadCommand(
            company_id=request.company_id,
            contact_id=request.contact_id,
            source=request.source.value,
            score=request.score,
            notes=request.notes,
        )

    @staticmethod
    def to_update_command(
        request: UpdateLeadRequestDTO,
        lead_id: str,
    ) -> UpdateLeadCommand:
        """Map update request DTO to command."""
        return UpdateLeadCommand(
            lead_id=lead_id,
            contact_id=request.contact_id,
            source=(request.source.value if request.source is not None else None),
            status=(request.status.value if request.status is not None else None),
            score=request.score,
            notes=request.notes,
        )

    @staticmethod
    def to_domain(
        command: CreateLeadCommand,
    ) -> Lead:
        """Map create command to Lead domain entity."""
        return Lead(
            id=LeadId(),
            company_id=CompanyId(command.company_id),
            contact_id=ContactId(command.contact_id),
            source=LeadSource(command.source),
            score=LeadScore(command.score),
            notes=command.notes,
            evidence_signals=command.evidence_signals,
        )

    @staticmethod
    def apply_update(
        lead: Lead,
        command: UpdateLeadCommand,
    ) -> None:
        """Apply Lead-owned command changes through domain operations."""
        if command.contact_id is not None:
            lead.update_contact(ContactId(command.contact_id))

        if command.source is not None:
            lead.update_source(LeadSource(command.source))

        if command.status is not None:
            lead.update_status(LeadStatus(command.status))

        if command.score is not None:
            lead.update_score(LeadScore(command.score))

        if command.notes is not None:
            lead.update_notes(command.notes)

    @staticmethod
    def to_response(
        lead: Lead,
    ) -> LeadResponseDTO:
        """Map Lead domain entity to response DTO."""
        return LeadResponseDTO(
            id=str(lead.id),
            company_id=str(lead.company_id),
            contact_id=str(lead.contact_id),
            source=lead.source,
            status=lead.status,
            score=lead.score.value,
            notes=lead.notes,
            is_qualified=lead.is_qualified,
            created_at=lead.created_at,
            updated_at=lead.updated_at,
            review_status=lead.review_status,
            review_submitted_at=lead.review_submitted_at,
            review_decided_at=lead.review_decided_at,
            review_notes=lead.review_notes,
            evidence_signals=lead.evidence_signals,
        )

    @staticmethod
    def to_response_list(
        leads: list[Lead],
    ) -> list[LeadResponseDTO]:
        """Map a Lead collection to response DTOs."""
        return [LeadMapper.to_response(lead) for lead in leads]
