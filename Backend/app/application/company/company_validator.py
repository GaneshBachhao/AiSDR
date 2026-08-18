"""
Company Application Validator.

Architecture Freeze v5.0
"""

from __future__ import annotations

from app.application.common.validation.validation_result import (
    ValidationResult,
)
from app.application.common.validation.validator import Validator
from app.application.company.company_commands import (
    CreateCompanyCommand,
    UpdateCompanyCommand,
)


class CompanyValidator(
    Validator[CreateCompanyCommand | UpdateCompanyCommand],
):
    """Validates Company commands."""

    def validate(
        self,
        request: CreateCompanyCommand | UpdateCompanyCommand,
    ) -> ValidationResult:
        result = ValidationResult()

        if isinstance(request, CreateCompanyCommand):
            if not request.name or not request.name.strip():
                result.add_error(
                    field="name",
                    message="Company name is required.",
                )
            elif len(request.name.strip()) < 2:
                result.add_error(
                    field="name",
                    message=("Company name must contain at least 2 characters."),
                )

        elif request.name is not None:
            if not request.name.strip():
                result.add_error(
                    field="name",
                    message="Company name is required.",
                )
            elif len(request.name.strip()) < 2:
                result.add_error(
                    field="name",
                    message=("Company name must contain at least 2 characters."),
                )

        if request.employee_count is not None and request.employee_count < 0:
            result.add_error(
                field="employee_count",
                message="Employee count cannot be negative.",
            )

        return result

    def validate_create(
        self,
        request: CreateCompanyCommand,
    ) -> ValidationResult:
        return self.validate(request)

    def validate_update(
        self,
        request: UpdateCompanyCommand,
    ) -> ValidationResult:
        return self.validate(request)
