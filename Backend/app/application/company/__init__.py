"""
Company Application Validator.

Architecture Freeze v4.1
"""

from __future__ import annotations

from app.application.common.validation.validation_result import (
    ValidationResult,
)
from app.application.common.validation.validator import (
    Validator,
)

from app.application.company.company_commands import (
    CreateCompanyCommand,
    UpdateCompanyCommand,
)


class CompanyValidator(
    Validator[
        CreateCompanyCommand | UpdateCompanyCommand
    ],
):
    """
    Validates Company commands.
    """

    def validate(
        self,
        request: CreateCompanyCommand | UpdateCompanyCommand,
    ) -> ValidationResult:
        """
        Validate company command.
        """

        result = ValidationResult()

        if isinstance(request, CreateCompanyCommand):
            if not request.name or not request.name.strip():
                result.add_error(
                    field="name",
                    message="Company name is required.",
                )
                return result

            if len(request.name.strip()) < 2:
                result.add_error(
                    field="name",
                    message=(
                        "Company name must contain at least "
                        "2 characters."
                    ),
                )

            self._validate_optional_text_fields(
                request,
                result,
            )

            return result

        if request.name is not None:
            if not request.name.strip():
                result.add_error(
                    field="name",
                    message="Company name is required.",
                )

            elif len(request.name.strip()) < 2:
                result.add_error(
                    field="name",
                    message=(
                        "Company name must contain at least "
                        "2 characters."
                    ),
                )

        self._validate_optional_text_fields(
            request,
            result,
        )

        return result

    @staticmethod
    def _validate_optional_text_fields(
        request: CreateCompanyCommand | UpdateCompanyCommand,
        result: ValidationResult,
    ) -> None:
        if request.industry is not None and not request.industry.strip():
            result.add_error(
                field="industry",
                message="Industry cannot be blank.",
            )

        if request.company_size is not None and not request.company_size.strip():
            result.add_error(
                field="company_size",
                message="Company size cannot be blank.",
            )