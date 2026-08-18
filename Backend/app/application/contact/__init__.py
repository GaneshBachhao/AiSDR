"""
Contact Application Validator.

Architecture Freeze v4.0

Validates:
- CreateContactCommand
- UpdateContactCommand

No:
- Repository access
- Database checks
- Domain logic
"""

from __future__ import annotations

from app.application.contact.contact_commands import (
    CreateContactCommand,
    UpdateContactCommand,
)


class ContactValidator:
    """
    Validates Contact commands.
    """

    @staticmethod
    def validate_create(
        command: CreateContactCommand,
    ) -> None:
        """
        Validate create contact command.
        """

        if not command.company_id.strip():
            raise ValueError("Company id is required.")

        if not command.first_name.strip():
            raise ValueError("First name is required.")

        if len(command.first_name.strip()) < 2:
            raise ValueError("First name must contain at least 2 characters.")

        if not command.last_name.strip():
            raise ValueError("Last name is required.")

        if len(command.last_name.strip()) < 2:
            raise ValueError("Last name must contain at least 2 characters.")

        if not command.email.strip():
            raise ValueError("Email is required.")

        if "@" not in command.email:
            raise ValueError("Email address is invalid.")

    @staticmethod
    def validate_update(
        command: UpdateContactCommand,
    ) -> None:
        """
        Validate update contact command.
        """

        if command.first_name is not None:
            if len(command.first_name.strip()) < 2:
                raise ValueError("First name must contain at least 2 characters.")

        if command.last_name is not None:
            if len(command.last_name.strip()) < 2:
                raise ValueError("Last name must contain at least 2 characters.")

        if command.email is not None:
            if "@" not in command.email:
                raise ValueError("Email address is invalid.")
