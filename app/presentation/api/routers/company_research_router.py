from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.application.company_research.dto.company_research_request import (
    CompanyResearchRequest,
)
from app.application.company_research.dto.company_research_response import (
    CompanySearchResult,
)
from app.infrastructure.ai.exceptions.ai_budget_exceeded_exception import (
    AIBudgetExceededException,
)
from app.presentation.api.dependencies.company_research import (
    SearchCompaniesHandlerDependency,
)

router = APIRouter(
    prefix="/company-research",
    tags=["Company Research"],
)


@router.post(
    "/search",
    response_model=list[CompanySearchResult],
    status_code=status.HTTP_200_OK,
)
async def search_companies(
    request: CompanyResearchRequest,
    handler: SearchCompaniesHandlerDependency,
) -> list[CompanySearchResult]:
    """Discover and research public-web company opportunities.

    This endpoint returns research candidates only. It does not create
    Company, Contact, Lead, or other CRM records and does not contact anyone.
    """
    try:
        return await handler.handle(request)
    except AIBudgetExceededException as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Company research failed: {exc}",
        ) from exc
