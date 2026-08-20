"""
Sequence Application Mapper.

Maps:
- Request DTO -> Command
- Command -> Domain Entity
- Domain Entity -> Response DTO
"""

from __future__ import annotations

from app.application.sequence.dto.sequence_requests import CreateSequenceRequestDTO
from app.application.sequence.dto.sequence_responses import (
    SequenceResponseDTO,
    TouchResponseDTO,
)
from app.application.sequence.sequence_commands import CreateSequenceCommand, TouchInput
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.sequence.entities.sequence import Sequence
from app.domain.sequence.value_objects.touch import Touch


class SequenceMapper:
    """Maps Sequence application and domain objects."""

    @staticmethod
    def to_create_command(request: CreateSequenceRequestDTO) -> CreateSequenceCommand:
        return CreateSequenceCommand(
            lead_id=request.lead_id,
            touches=[
                TouchInput(channel=touch.channel, wait_days=touch.wait_days) for touch in request.touches
            ],
        )

    @staticmethod
    def to_domain(command: CreateSequenceCommand) -> Sequence:
        return Sequence(
            lead_id=LeadId(command.lead_id),
            touches=[Touch(channel=touch.channel, wait_days=touch.wait_days) for touch in command.touches],
        )

    @staticmethod
    def to_response(sequence: Sequence) -> SequenceResponseDTO:
        return SequenceResponseDTO(
            id=str(sequence.id),
            lead_id=str(sequence.lead_id),
            touches=[
                TouchResponseDTO(channel=touch.channel, wait_days=touch.wait_days)
                for touch in sequence.touches
            ],
            status=sequence.status,
            current_touch_index=sequence.current_touch_index,
            started_at=sequence.started_at,
            ended_at=sequence.ended_at,
            stop_reason=sequence.stop_reason,
            next_touch_due_at=sequence.next_touch_due_at(),
            created_at=sequence.created_at,
            updated_at=sequence.updated_at,
        )

    @staticmethod
    def to_response_list(sequences: list[Sequence]) -> list[SequenceResponseDTO]:
        return [SequenceMapper.to_response(sequence) for sequence in sequences]
