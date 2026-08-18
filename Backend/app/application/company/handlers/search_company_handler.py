"""
Search Companies application handler.
"""

from __future__ import annotations

from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.company.company_mapper import CompanyMapper
from app.application.company.company_queries import SearchCompaniesQuery
from app.application.company.dto.company_responses import CompanyResponseDTO


class SearchCompanyHandler:
    """Handles Search Companies use case."""

    def __init__(self, unit_of_work: UnitOfWork, mapper: CompanyMapper) -> None:
        self._unit_of_work = unit_of_work
        self._mapper = mapper

    async def handle(
        self,
        query: SearchCompaniesQuery,
    ) -> list[CompanyResponseDTO]:
        async with self._unit_of_work:
            companies = await self._unit_of_work.company_repository.search(
                search_text=query.search_text,
                skip=query.skip,
                limit=query.limit,
            )

        return self._mapper.to_response_list(companies)
