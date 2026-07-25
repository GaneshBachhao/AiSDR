# app/application/assessment/commands/start_assessment.py

"""
Start Assessment command.
"""

from __future__ import annotations

from uuid import UUID

from app.application.common.commands.command import (
    Command,
)


class StartAssessmentCommand(Command):
    """
    Request to start an assessment for a discovery session.
    """

    discovery_session_id: UUID

    summary: str | None = None