"""
Outcome Application Mapper.

Maps:
- Request DTO -> Command
- Command -> Domain Entity
- Domain Entity -> Response DTO
"""

from __future__ import annotations

from app.application.outcome.dto.outcome_requests import (
    CreateOutcomeEventRequestDTO,
)
from app.application.outcome.dto.outcome_responses import (
    OutcomeEventResponseDTO,
)
from app.application.outcome.outcome_commands import CreateOutcomeEventCommand
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.outcome.entities.outcome_event import OutcomeEvent


class OutcomeMapper:
    """Maps Outcome application and domain objects."""

    @staticmethod
    def to_create_command(
        request: CreateOutcomeEventRequestDTO,
    ) -> CreateOutcomeEventCommand:
        return CreateOutcomeEventCommand(
            lead_id=request.lead_id,
            outcome_type=request.outcome_type,
            occurred_at=request.occurred_at,
            notes=request.notes,
        )

    @staticmethod
    def to_domain(command: CreateOutcomeEventCommand) -> OutcomeEvent:
        kwargs = {
            "lead_id": LeadId(command.lead_id),
            "outcome_type": command.outcome_type,
            "notes": command.notes,
        }
        if command.occurred_at is not None:
            kwargs["occurred_at"] = command.occurred_at
        return OutcomeEvent(**kwargs)

    @staticmethod
    def to_response(event: OutcomeEvent) -> OutcomeEventResponseDTO:
        return OutcomeEventResponseDTO(
            id=str(event.id),
            lead_id=str(event.lead_id),
            outcome_type=event.outcome_type,
            notes=event.notes,
            occurred_at=event.occurred_at,
            created_at=event.created_at,
            updated_at=event.updated_at,
        )

    @staticmethod
    def to_response_list(
        events: list[OutcomeEvent],
    ) -> list[OutcomeEventResponseDTO]:
        return [OutcomeMapper.to_response(event) for event in events]
