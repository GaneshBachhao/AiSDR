"""
Discovery application commands.

Architecture Freeze v5.0
"""

from __future__ import annotations

from app.application.common.commands.command import Command


class CreateDiscoveryCommand(Command):
    """Command to create a discovery session."""

    lead_id: str
    problem_statement: str | None = None
    current_solution: str | None = None
    business_impact: str | None = None
    success_criteria: str | None = None


class UpdateDiscoveryCommand(Command):
    """Command to update a discovery session."""

    discovery_id: str
    problem_statement: str | None = None
    current_solution: str | None = None
    business_impact: str | None = None
    success_criteria: str | None = None
    status: str | None = None


class DeleteDiscoveryCommand(Command):
    """Command to delete a discovery session."""

    discovery_id: str
