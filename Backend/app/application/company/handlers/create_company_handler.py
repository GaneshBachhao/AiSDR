"""
Create Company application handler.
Architecture Freeze v5.0

Transaction rule:
- The handler owns the Company create use-case transaction boundary.
- Repository operations are staged in the shared UnitOfWork.
- The transaction is explicitly committed before returning the response.
- Other aggregates/domains are not modified by this handler.
"""

from __future__ import annotations

from sqlalchemy.exc import IntegrityError

from app.application.common.exceptions.conflict_exception import ConflictException
from app.application.common.exceptions.validation_exception import ValidationException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.company.company_commands import CreateCompanyCommand
from app.application.company.company_mapper import CompanyMapper
from app.application.company.company_validator import CompanyValidator
from app.application.company.dto.company_responses import CompanyResponseDTO


class CreateCompanyHandler:
    """Handles the Create Company use case."""

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        validator: CompanyValidator,
        mapper: CompanyMapper,
    ) -> None:
        self._unit_of_work = unit_of_work
        self._validator = validator
        self._mapper = mapper

    async def handle(
        self,
        command: CreateCompanyCommand,
    ) -> CompanyResponseDTO:
        validation = self._validator.validate_create(command)
        if not validation.is_valid:
            raise ValidationException(
                message="Company validation failed.",
                details={error.field: error.message for error in validation.errors},
            )

        company = self._mapper.to_domain(command)

        try:
            async with self._unit_of_work:
                repository = self._unit_of_work.company_repository

                existing_company = await repository.find_by_name(
                    command.name,
                )
                if existing_company is not None:
                    raise ConflictException(
                        message="Company already exists.",
                        details={"name": command.name.strip()},
                    )

                await repository.add(company)
                await self._unit_of_work.commit()

        except IntegrityError as exc:
            if "UNIQUE constraint failed: companies.name" in str(exc):
                raise ConflictException(
                    message="Company already exists.",
                    details={"name": command.name.strip()},
                ) from exc
            raise

        return self._mapper.to_response(company)
