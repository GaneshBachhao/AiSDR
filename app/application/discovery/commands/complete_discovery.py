"""
Complete Discovery command.
"""

from __future__ import annotations

from uuid import UUID

from app.application.common.commands.command import (
    Command,
)


class CompleteDiscoveryCommand(Command):
    """
    Request to complete a discovery session.
    """

    discovery_session_id: UUID

    summary: str | None = None