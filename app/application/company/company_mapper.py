"""
Company Application Mapper.

Architecture Freeze v5.0

Maps:
- Request DTO -> Command
- Domain Entity -> Response DTO
"""

from __future__ import annotations

import re

from app.application.company.company_commands import (
    CreateCompanyCommand,
    UpdateCompanyCommand,
)
from app.application.company.dto.company_requests import (
    CreateCompanyRequestDTO,
    UpdateCompanyRequestDTO,
)
from app.application.company.dto.company_responses import (
    CompanyResponseDTO,
)
from app.domain.company.entities.company import Company
from app.domain.company.value_objects.company_size import CompanySize
from app.domain.company.value_objects.industry import Industry


class CompanyMapper:
    """Maps Company application objects."""

    @staticmethod
    def _normalize_text(value: str) -> str:
        return " ".join(
            value.strip().replace("_", " ").replace("-", " ").split()
        ).lower()

    @staticmethod
    def _to_industry(
        value: str | Industry | None,
    ) -> Industry | None:
        if value is None or isinstance(value, Industry):
            return value

        try:
            return Industry(value)
        except ValueError:
            normalized = CompanyMapper._normalize_text(value)
            aliases = {
                "ai": Industry.INFORMATION_TECHNOLOGY,
                "a i": Industry.INFORMATION_TECHNOLOGY,
                "artificial intelligence": Industry.INFORMATION_TECHNOLOGY,
                "machine learning": Industry.INFORMATION_TECHNOLOGY,
                "software": Industry.INFORMATION_TECHNOLOGY,
                "saas": Industry.INFORMATION_TECHNOLOGY,
                "it": Industry.INFORMATION_TECHNOLOGY,
                "information technology": Industry.INFORMATION_TECHNOLOGY,
                "fintech": Industry.FINANCIAL_SERVICES,
                "proptech": Industry.REAL_ESTATE,
                "edtech": Industry.EDUCATION,
                "agritech": Industry.AGRICULTURE,
                "govtech": Industry.GOVERNMENT,
                "telecom": Industry.TELECOMMUNICATIONS,
            }
            return aliases.get(normalized, Industry.OTHER)

    @staticmethod
    def _to_company_size(
        value: str | CompanySize | None,
    ) -> CompanySize | None:
        if value is None or isinstance(value, CompanySize):
            return value

        try:
            return CompanySize(value)
        except ValueError:
            normalized = CompanyMapper._normalize_text(value)
            aliases = {
                "micro": CompanySize.MICRO,
                "solo": CompanySize.MICRO,
                "startup": CompanySize.MICRO,
                "small": CompanySize.SMALL,
                "medium": CompanySize.MEDIUM,
                "large": CompanySize.LARGE,
                "enterprise": CompanySize.ENTERPRISE,
            }

            if normalized in aliases:
                return aliases[normalized]

            numbers = [
                int(match)
                for match in re.findall(r"\d+", normalized)
            ]

            if numbers:
                upper_bound = numbers[-1]
                if "+" in normalized and len(numbers) == 1:
                    upper_bound = numbers[0]

                if upper_bound <= 10:
                    return CompanySize.MICRO
                if upper_bound <= 50:
                    return CompanySize.SMALL
                if upper_bound <= 250:
                    return CompanySize.MEDIUM
                if upper_bound <= 1000:
                    return CompanySize.LARGE
                return CompanySize.ENTERPRISE

            return None

    @staticmethod
    def create_request_to_command(
        request: CreateCompanyRequestDTO,
    ) -> CreateCompanyCommand:
        return CreateCompanyCommand(
            name=request.name,
            website=request.website,
            industry=CompanyMapper._to_industry(request.industry),
            company_size=CompanyMapper._to_company_size(request.company_size),
            employee_count=request.employee_count,
            country=request.country,
            state=request.state,
            city=request.city,
        )

    @staticmethod
    def update_request_to_command(
        request: UpdateCompanyRequestDTO,
        company_id: str,
    ) -> UpdateCompanyCommand:
        return UpdateCompanyCommand(
            company_id=company_id,
            name=request.name,
            website=request.website,
            industry=CompanyMapper._to_industry(request.industry),
            company_size=CompanyMapper._to_company_size(request.company_size),
            employee_count=request.employee_count,
            country=request.country,
            state=request.state,
            city=request.city,
        )

    @staticmethod
    def to_domain(
        command: CreateCompanyCommand,
    ) -> Company:
        return Company(
            name=command.name,
            website=command.website,
            industry=CompanyMapper._to_industry(command.industry),
            company_size=CompanyMapper._to_company_size(command.company_size),
            employee_count=command.employee_count,
            country=command.country,
            state=command.state,
            city=command.city,
        )

    @staticmethod
    def to_response(
        company: Company,
    ) -> CompanyResponseDTO:
        return CompanyResponseDTO(
            id=str(company.id.value),
            name=company.name,
            website=company.website,
            industry=(
                company.industry.value
                if company.industry is not None
                else None
            ),
            company_size=(
                company.company_size.value
                if company.company_size is not None
                else None
            ),
            employee_count=company.employee_count,
            country=company.country,
            state=company.state,
            city=company.city,
            is_active=company.is_active,
        )

    @staticmethod
    def to_response_list(
        companies: list[Company],
    ) -> list[CompanyResponseDTO]:
        return [
            CompanyMapper.to_response(company)
            for company in companies
        ]
