"""
Generate Assessment Command.
"""

from __future__ import annotations

from uuid import UUID

from app.application.common.commands.command import Command


class GenerateAssessmentCommand(Command):
    """
    Request to generate an assessment for a discovery session.
    """

    discovery_session_id: UUID