"""
Update Company application handler.
"""
from __future__ import annotations

from sqlalchemy.exc import IntegrityError

from app.application.common.exceptions.conflict_exception import ConflictException
from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.exceptions.validation_exception import ValidationException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.company.company_commands import UpdateCompanyCommand
from app.application.company.company_mapper import CompanyMapper
from app.application.company.company_validator import CompanyValidator
from app.application.company.dto.company_responses import CompanyResponseDTO
from app.domain.company.identifiers.company_id import CompanyId


class UpdateCompanyHandler:
    """Handles Update Company use case."""

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
        command: UpdateCompanyCommand,
    ) -> CompanyResponseDTO:
        validation = self._validator.validate_update(command)
        if not validation.is_valid:
            raise ValidationException(
                message="Company validation failed.",
                details={
                    error.field: error.message
                    for error in validation.errors
                },
            )

        try:
            company_id = CompanyId(command.company_id)
        except (TypeError, ValueError) as exc:
            raise ValidationException(
                message="Invalid company id.",
                details={"company_id": command.company_id},
            ) from exc

        try:
            async with self._unit_of_work:
                repository = self._unit_of_work.company_repository
                company = await repository.get_by_id(company_id)

                if company is None:
                    raise NotFoundException(
                        message="Company not found.",
                        details={"company_id": command.company_id},
                    )

                if command.name is not None:
                    existing_company = await repository.find_by_name(
                        command.name,
                    )
                    if (
                        existing_company is not None
                        and existing_company.id != company.id
                    ):
                        raise ConflictException(
                            message="Company already exists.",
                            details={"name": command.name.strip()},
                        )
                    company.update_name(command.name)

                if command.website is not None:
                    company.update_website(command.website)

                if command.industry is not None:
                    company.update_industry(
                        self._mapper._to_industry(command.industry)
                    )

                if command.company_size is not None:
                    company.update_company_size(
                        self._mapper._to_company_size(command.company_size)
                    )

                if command.employee_count is not None:
                    company.update_employee_count(
                        command.employee_count
                    )

                if (
                    command.country is not None
                    or command.state is not None
                    or command.city is not None
                ):
                    company.update_location(
                        country=command.country,
                        state=command.state,
                        city=command.city,
                    )

                await repository.update(company)
                await self._unit_of_work.commit()

        except IntegrityError as exc:
            if "UNIQUE constraint failed: companies.name" in str(exc):
                raise ConflictException(
                    message="Company already exists.",
                    details={"name": command.name.strip() if command.name else None},
                ) from exc
            raise

        return self._mapper.to_response(company)
