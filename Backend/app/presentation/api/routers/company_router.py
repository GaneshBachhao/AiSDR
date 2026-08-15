"""
Company API routes.

Architecture Freeze v5.0
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi import Query
from fastapi import Response
from fastapi import status

from app.application.company.company_commands import (
    CreateCompanyCommand,
    DeleteCompanyCommand,
    UpdateCompanyCommand,
)
from app.application.company.company_queries import (
    GetCompanyQuery,
    ListCompaniesQuery,
    SearchCompaniesQuery,
)
from app.application.company.dto.company_requests import (
    CreateCompanyRequestDTO,
    UpdateCompanyRequestDTO,
)
from app.application.company.dto.company_responses import (
    CompanyResponseDTO,
)
from app.presentation.api.dependencies.handlers import (
    CreateCompanyHandlerDependency,
    DeleteCompanyHandlerDependency,
    GetCompanyHandlerDependency,
    ListCompanyHandlerDependency,
    SearchCompanyHandlerDependency,
    UpdateCompanyHandlerDependency,
)

router = APIRouter(
    prefix="/companies",
    tags=["Companies"],
)


@router.post(
    "",
    response_model=CompanyResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
async def create_company(
    request: CreateCompanyRequestDTO,
    handler: CreateCompanyHandlerDependency,
) -> CompanyResponseDTO:
    command = CreateCompanyCommand(
        name=request.name,
        website=request.website,
        industry=request.industry,
        company_size=request.company_size,
        employee_count=request.employee_count,
        country=request.country,
        state=request.state,
        city=request.city,
    )
    return await handler.handle(command)


@router.get(
    "",
    response_model=list[CompanyResponseDTO],
)
async def list_companies(
    handler: ListCompanyHandlerDependency,
    skip: int = 0,
    limit: int = 100,
) -> list[CompanyResponseDTO]:
    query = ListCompaniesQuery(skip=skip, limit=limit)
    return await handler.handle(query)


@router.get(
    "/search",
    response_model=list[CompanyResponseDTO],
)
async def search_companies(
    handler: SearchCompanyHandlerDependency,
    query: str = Query(...),
    skip: int = 0,
    limit: int = 100,
) -> list[CompanyResponseDTO]:
    search_query = SearchCompaniesQuery(
        search_text=query,
        skip=skip,
        limit=limit,
    )
    return await handler.handle(search_query)


@router.get(
    "/{company_id}",
    response_model=CompanyResponseDTO,
)
async def get_company(
    company_id: str,
    handler: GetCompanyHandlerDependency,
) -> CompanyResponseDTO:
    query = GetCompanyQuery(company_id=company_id)
    return await handler.handle(query)


@router.put(
    "/{company_id}",
    response_model=CompanyResponseDTO,
)
async def update_company(
    company_id: str,
    request: UpdateCompanyRequestDTO,
    handler: UpdateCompanyHandlerDependency,
) -> CompanyResponseDTO:
    command = UpdateCompanyCommand(
        company_id=company_id,
        name=request.name,
        website=request.website,
        industry=request.industry,
        company_size=request.company_size,
        employee_count=request.employee_count,
        country=request.country,
        state=request.state,
        city=request.city,
    )
    return await handler.handle(command)


@router.delete(
    "/{company_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_company(
    company_id: str,
    handler: DeleteCompanyHandlerDependency,
) -> Response:
    command = DeleteCompanyCommand(company_id=company_id)
    await handler.handle(command)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
