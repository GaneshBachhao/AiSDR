from __future__ import annotations

import re

from app.application.common.validation.validation_result import ValidationResult
from app.application.lead.commands.create_lead import (
    CreateLeadCommand,
)

class CreateLeadValidator:
    """
    Validates CreateLeadCommand.

    This validator performs only application-level validation.
    Business rules belong in the domain layer.
    """

    EMAIL_PATTERN = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    WEBSITE_PATTERN = re.compile(
        r"^https?://.+"
    )

    def validate(
        self,
        command: CreateLeadCommand,
    ) -> ValidationResult:
        """
        Validate the incoming command.
        """
        result = ValidationResult()

        if not command.company_name.strip():
            result.add_error(
                "company_name",
                "Company name is required.",
            )

        if not command.contact_name.strip():
            result.add_error(
                "contact_name",
                "Contact name is required.",
            )

        if not command.email.strip():
            result.add_error(
                "email",
                "Email is required.",
            )
        elif not self.EMAIL_PATTERN.match(command.email):
            result.add_error(
                "email",
                "Invalid email address.",
            )

        if (
            command.website
            and not self.WEBSITE_PATTERN.match(command.website)
        ):
            result.add_error(
                "website",
                "Website must start with http:// or https://",
            )

        if (
            command.phone
            and len(command.phone.strip()) < 7
        ):
            result.add_error(
                "phone",
                "Phone number is invalid.",
            )

        return result