"""
Outcome application commands.

Commands represent write operations on the OutcomeEvent aggregate.
"""

from __future__ import annotations

from datetime import datetime

from app.application.common.commands.command import Command
from app.domain.outcome.enums.outcome_type import OutcomeType


class CreateOutcomeEventCommand(Command):
    """Command to record an outcome for a Lead."""

    lead_id: str
    outcome_type: OutcomeType
    occurred_at: datetime | None = None
    notes: str | None = None


class DeleteOutcomeEventCommand(Command):
    """Command to remove a mis-logged outcome."""

    outcome_id: str
