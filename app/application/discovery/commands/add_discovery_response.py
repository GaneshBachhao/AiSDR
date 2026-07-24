"""
Add Discovery Response command.
"""

from __future__ import annotations

from uuid import UUID

from app.application.common.commands.command import (
    Command,
)


class AddDiscoveryResponseCommand(Command):
    """
    Request to add a response to a discovery session.
    """

    discovery_session_id: UUID

    question_id: str

    question: str

    answer: str

    response_type: str = "TEXT"

    confidence: float = 1.0

    remarks: str | None = None