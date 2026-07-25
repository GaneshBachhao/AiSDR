"""
Create Lead command.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.common.commands.command import (
    Command,
)


@dataclass
class CreateLeadCommand(Command):
    """
    Request to create a new lead.
    """

    company_name: str

    contact_name: str

    email: str

    phone: str | None = None

    website: str | None = None