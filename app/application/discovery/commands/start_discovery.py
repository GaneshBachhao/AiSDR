"""
Start Discovery command.
"""

from __future__ import annotations

from uuid import UUID

from app.application.common.commands.command import (
    Command,
)


class StartDiscoveryCommand(Command):
    """
    Request to start a discovery session.
    """

    lead_id: UUID

    company_id: str | None = None