"""
Contact Application Validator.

Architecture Freeze v5.0
"""

from __future__ import annotations

from app.application.common.validation.validation_result import (
    ValidationResult,
)
from app.application.common.validation.validator import (
    Validator,
)
from app.application.contact.contact_commands import (
    CreateContactCommand,
    UpdateContactCommand,
)


class ContactValidator(
    Validator[CreateContactCommand | UpdateContactCommand],
):
    """Validates Contact application commands."""

    def validate(
        self,
        request: CreateContactCommand | UpdateContactCommand,
    ) -> ValidationResult:
        """Validate a Contact command."""
        result = ValidationResult()

        if isinstance(request, CreateContactCommand):
            if not request.company_id or not request.company_id.strip():
                result.add_error(
                    field="company_id",
                    message="Company id is required.",
                )

            if not request.first_name or not request.first_name.strip():
                result.add_error(
                    field="first_name",
                    message="First name is required.",
                )
            elif len(request.first_name.strip()) < 2:
                result.add_error(
                    field="first_name",
                    message="First name must contain at least 2 characters.",
                )

            if not request.last_name or not request.last_name.strip():
                result.add_error(
                    field="last_name",
                    message="Last name is required.",
                )
            elif len(request.last_name.strip()) < 2:
                result.add_error(
                    field="last_name",
                    message="Last name must contain at least 2 characters.",
                )

            if not request.email or not request.email.strip():
                result.add_error(
                    field="email",
                    message="Email is required.",
                )

            return result

        if not request.contact_id or not request.contact_id.strip():
            result.add_error(
                field="contact_id",
                message="Contact id is required.",
            )

        if request.first_name is not None:
            if not request.first_name.strip():
                result.add_error(
                    field="first_name",
                    message="First name cannot be empty.",
                )
            elif len(request.first_name.strip()) < 2:
                result.add_error(
                    field="first_name",
                    message="First name must contain at least 2 characters.",
                )

        if request.last_name is not None:
            if not request.last_name.strip():
                result.add_error(
                    field="last_name",
                    message="Last name cannot be empty.",
                )
            elif len(request.last_name.strip()) < 2:
                result.add_error(
                    field="last_name",
                    message="Last name must contain at least 2 characters.",
                )

        if request.email is not None and not request.email.strip():
            result.add_error(
                field="email",
                message="Email cannot be empty.",
            )

        return result

    def validate_create(
        self,
        request: CreateContactCommand,
    ) -> ValidationResult:
        """Validate a create Contact command."""
        return self.validate(request)

    def validate_update(
        self,
        request: UpdateContactCommand,
    ) -> ValidationResult:
        """Validate an update Contact command."""
        return self.validate(request)
