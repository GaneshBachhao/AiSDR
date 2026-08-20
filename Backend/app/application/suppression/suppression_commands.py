"""
Suppression application commands.

Commands represent write operations on the SuppressionEntry aggregate.
"""

from __future__ import annotations

from app.application.common.commands.command import Command
from app.domain.suppression.enums.suppression_reason import SuppressionReason


class CreateSuppressionCommand(Command):
    """Command to manually add an email to the do-not-contact list."""

    email: str
    reason: SuppressionReason = SuppressionReason.MANUAL
    notes: str | None = None


class DeleteSuppressionCommand(Command):
    """Command to lift a suppression."""

    suppression_id: str


class RecordEmailEventCommand(Command):
    """Command to auto-suppress on a bounce/complaint event."""

    email: str
    event_type: str
    reason: str | None = None
