# app/application/assessment/commands/add_finding.py

"""
Add Finding command.
"""

from __future__ import annotations

from uuid import UUID

from app.application.common.commands.command import (
    Command,
)


class AddFindingCommand(Command):
    """
    Request to add a finding to an assessment.
    """

    assessment_id: UUID

    title: str

    description: str

    finding_type: str

    severity: int = 3

    recommendation_hint: str | None = None