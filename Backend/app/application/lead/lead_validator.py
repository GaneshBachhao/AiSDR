"""
Lead Application Validator.

Architecture Freeze v5.0
"""

from __future__ import annotations

from uuid import UUID

from app.application.lead.lead_commands import (
    CreateLeadCommand,
    UpdateLeadCommand,
)
from app.domain.lead.enums.lead_source import LeadSource
from app.domain.lead.enums.lead_status import LeadStatus


class LeadValidator:
    """Validate Lead commands without repository/database access."""

    @staticmethod
    def _validate_uuid(value: str, field: str) -> None:
        try:
            UUID(str(value))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{field} must be a valid UUID.") from exc

    @staticmethod
    def validate_create(command: CreateLeadCommand) -> None:
        """Validate a create Lead command."""
        LeadValidator._validate_uuid(command.company_id, "company_id")
        LeadValidator._validate_uuid(command.contact_id, "contact_id")

        if command.source not in {item.value for item in LeadSource}:
            raise ValueError("Invalid lead source.")

        if command.notes is not None and not command.notes.strip():
            raise ValueError("notes cannot be blank.")

    @staticmethod
    def validate_update(command: UpdateLeadCommand) -> None:
        """Validate an update Lead command."""
        LeadValidator._validate_uuid(command.lead_id, "lead_id")

        if command.contact_id is not None:
            LeadValidator._validate_uuid(command.contact_id, "contact_id")

        if command.source is not None and command.source not in {item.value for item in LeadSource}:
            raise ValueError("Invalid lead source.")

        if command.status is not None and command.status not in {item.value for item in LeadStatus}:
            raise ValueError("Invalid lead status.")

        if command.score is not None and not 0 <= command.score <= 100:
            raise ValueError("Lead score must be between 0 and 100.")

        if command.notes is not None and not command.notes.strip():
            raise ValueError("notes cannot be blank.")
