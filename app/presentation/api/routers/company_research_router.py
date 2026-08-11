from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.company_research.schemas.company_research import (
    CompanyResearchRequest,
    CompanySearchResult,
)
from app.company_research.services.company_research_service import (
    CompanyResearchService,
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
) -> list[CompanySearchResult]:
    """Discover and research public-web company opportunities.

    This endpoint returns research candidates only. It does not create
    Company, Contact, Lead, or other CRM records and does not contact anyone.
    """
    try:
        service = CompanyResearchService()
        return service.search(request)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Company research failed: {exc}",
        ) from exc
