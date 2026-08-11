"""
Lead application commands.

Architecture Freeze v5.0
Commands represent write operations on the Lead aggregate.
"""

from __future__ import annotations

from app.application.common.commands.command import Command


class CreateLeadCommand(Command):
    """Command to create a Lead."""

    company_id: str
    contact_id: str
    source: str = "Other"
    score: int = 0
    notes: str | None = None


class UpdateLeadCommand(Command):
    """Command to update Lead-owned information."""

    lead_id: str
    contact_id: str | None = None
    source: str | None = None
    status: str | None = None
    score: int | None = None
    notes: str | None = None


class DeleteLeadCommand(Command):
    """Command to delete a Lead."""

    lead_id: str
