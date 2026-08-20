"""
Suppression Application Mapper.

Maps:
- Request DTO -> Command
- Command -> Domain Entity
- Domain Entity -> Response DTO
"""

from __future__ import annotations

from app.application.suppression.dto.suppression_requests import (
    CreateSuppressionRequestDTO,
)
from app.application.suppression.dto.suppression_responses import (
    SuppressionEntryResponseDTO,
)
from app.application.suppression.suppression_commands import CreateSuppressionCommand
from app.domain.contact.value_objects.email import Email
from app.domain.suppression.entities.suppression_entry import SuppressionEntry


class SuppressionMapper:
    """Maps Suppression application and domain objects."""

    @staticmethod
    def to_create_command(
        request: CreateSuppressionRequestDTO,
    ) -> CreateSuppressionCommand:
        return CreateSuppressionCommand(
            email=request.email,
            reason=request.reason,
            notes=request.notes,
        )

    @staticmethod
    def to_domain(command: CreateSuppressionCommand) -> SuppressionEntry:
        return SuppressionEntry(
            email=Email(command.email),
            reason=command.reason,
            notes=command.notes,
        )

    @staticmethod
    def to_response(entry: SuppressionEntry) -> SuppressionEntryResponseDTO:
        return SuppressionEntryResponseDTO(
            id=str(entry.id),
            email=entry.email.value,
            reason=entry.reason,
            notes=entry.notes,
            suppressed_at=entry.suppressed_at,
            created_at=entry.created_at,
            updated_at=entry.updated_at,
        )

    @staticmethod
    def to_response_list(
        entries: list[SuppressionEntry],
    ) -> list[SuppressionEntryResponseDTO]:
        return [SuppressionMapper.to_response(entry) for entry in entries]
