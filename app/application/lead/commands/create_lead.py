# app/application/lead/commands/create_lead.py

"""
Create Lead command.
"""

from __future__ import annotations

from app.application.common.commands.command import (
    Command,
)


class CreateLeadCommand(Command):
    """
    Request to create a new lead.
    """

    company_name: str

    contact_name: str

    email: str

    phone: str | None = None

    website: str | None = None