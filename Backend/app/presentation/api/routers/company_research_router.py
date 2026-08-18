from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.application.company_research.dto.company_research_request import (
    CompanyResearchRequest,
)
from app.application.company_research.dto.company_research_response import (
    CandidateResearchFailure,
    CompanyResearchBatchResult,
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


class RetryCandidateRequest(BaseModel):
    """Input for ``POST /company-research/retry``.

    ``request`` should be the same research request the failed candidate
    originally came from (industries/geography/services/... drive evidence
    queries and scoring), so it's carried alongside the failure rather than
    assumed to be reconstructable from the failure alone.
    """

    failure: CandidateResearchFailure
    request: CompanyResearchRequest


@router.post(
    "/search",
    response_model=CompanyResearchBatchResult,
    status_code=status.HTTP_200_OK,
)
async def search_companies(
    request: CompanyResearchRequest,
    handler: SearchCompaniesHandlerDependency,
) -> CompanyResearchBatchResult:
    """Discover and research public-web company opportunities.

    This endpoint returns research candidates only. It does not create
    Company, Contact, Lead, or other CRM records and does not contact anyone.

    ``results`` are qualified candidates. ``failures`` are candidates whose
    identity-verification or evidence-gathering step raised unexpectedly
    (a network/provider error) before a qualification decision could be
    made -- distinct from a candidate that was checked and simply didn't
    qualify, which appears in neither list. Retry a failure via
    ``POST /company-research/retry`` without re-running discovery.
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


@router.post(
    "/retry",
    response_model=CompanySearchResult | CandidateResearchFailure | None,
    status_code=status.HTTP_200_OK,
)
async def retry_candidate(
    body: RetryCandidateRequest,
    handler: SearchCompaniesHandlerDependency,
) -> CompanySearchResult | CandidateResearchFailure | None:
    """Re-run research for one candidate from a prior ``failures`` entry.

    Skips discovery -- reconstructs the candidate from the failure's own
    fields. Returns a qualified result, another failure (if it fails again),
    or ``null`` if the candidate turns out not to qualify after all.
    """
    try:
        return await handler.retry_candidate(body.failure, body.request)
    except AIBudgetExceededException as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Candidate retry failed: {exc}",
        ) from exc
