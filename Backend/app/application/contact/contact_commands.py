"""
Contact Commands.

Contains all commands related to Contact aggregate.

Architecture Freeze v4.0
- Commands live at aggregate application root.
- Commands carry request data only.
- Handlers execute business workflow.
"""

from __future__ import annotations

from app.application.common.commands.command import (
    Command,
)


class CreateContactCommand(Command):
    """
    Command to create a contact.
    """

    company_id: str

    first_name: str

    last_name: str

    email: str

    phone: str | None = None

    job_title: str | None = None

    linkedin_url: str | None = None


class UpdateContactCommand(Command):
    """
    Command to update a contact.
    """

    contact_id: str

    first_name: str | None = None

    last_name: str | None = None

    email: str | None = None

    phone: str | None = None

    job_title: str | None = None

    linkedin_url: str | None = None


class DeleteContactCommand(Command):
    """
    Command to delete a contact.
    """

    contact_id: str
