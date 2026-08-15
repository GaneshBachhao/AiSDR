"""
Get Company application handler.
"""
from __future__ import annotations

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.exceptions.validation_exception import ValidationException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.company.company_mapper import CompanyMapper
from app.application.company.company_queries import GetCompanyQuery
from app.application.company.dto.company_responses import CompanyResponseDTO
from app.domain.company.identifiers.company_id import CompanyId


class GetCompanyHandler:
    """Handles Get Company use case."""

    def __init__(self, unit_of_work: UnitOfWork, mapper: CompanyMapper) -> None:
        self._unit_of_work = unit_of_work
        self._mapper = mapper

    async def handle(self, query: GetCompanyQuery) -> CompanyResponseDTO:
        try:
            company_id = CompanyId(query.company_id)
        except (TypeError, ValueError) as exc:
            raise ValidationException(
                message="Invalid company id.",
                details={"company_id": query.company_id},
            ) from exc

        async with self._unit_of_work:
            company = await self._unit_of_work.company_repository.get_by_id(company_id)
            if company is None:
                raise NotFoundException(
                    message="Company not found.",
                    details={"company_id": query.company_id},
                )

        return self._mapper.to_response(company)
