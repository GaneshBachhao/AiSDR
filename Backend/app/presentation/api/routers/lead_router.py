"""
Lead API router.

Architecture Freeze v5.0
"""

from __future__ import annotations

from fastapi import APIRouter, Query, Response, status

from app.application.compliance.dto.compliance_responses import (
    LeadComplianceRulesetResponseDTO,
)
from app.application.lead.dto.lead_requests import (
    ClassifyReplyRequestDTO,
    CreateLeadRequestDTO,
    LeadReviewDecisionRequestDTO,
    UpdateLeadRequestDTO,
)
from app.application.lead.dto.lead_responses import LeadResponseDTO
from app.application.lead.dto.lead_review_chain_response import LeadReviewChainResponseDTO
from app.application.lead.dto.reply_classification_responses import (
    ReplyClassificationResponseDTO,
)
from app.application.lead.lead_commands import (
    ApproveLeadCommand,
    ClassifyReplyCommand,
    DeleteLeadCommand,
    RejectLeadCommand,
    SubmitLeadForReviewCommand,
)
from app.application.lead.lead_mapper import LeadMapper
from app.application.lead.lead_queries import (
    GetLeadQuery,
    ListLeadQuery,
    SearchLeadQuery,
)
from app.presentation.api.dependencies.handlers import (
    ApproveLeadHandlerDependency,
    ClassifyReplyHandlerDependency,
    CreateLeadHandlerDependency,
    DeleteLeadHandlerDependency,
    GetLeadComplianceRulesetHandlerDependency,
    GetLeadHandlerDependency,
    GetLeadReviewChainHandlerDependency,
    ListLeadHandlerDependency,
    RejectLeadHandlerDependency,
    SearchLeadHandlerDependency,
    SubmitLeadForReviewHandlerDependency,
    UpdateLeadHandlerDependency,
)

router = APIRouter(
    prefix="/leads",
    tags=["Leads"],
)


@router.post(
    "",
    response_model=LeadResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
async def create_lead(
    request: CreateLeadRequestDTO,
    handler: CreateLeadHandlerDependency,
) -> LeadResponseDTO:
    """Create a Lead."""
    return await handler.handle(
        LeadMapper.to_create_command(request),
    )


@router.get(
    "",
    response_model=list[LeadResponseDTO],
)
async def list_leads(
    handler: ListLeadHandlerDependency,
    company_id: str | None = Query(default=None),
    contact_id: str | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
) -> list[LeadResponseDTO]:
    """List Leads."""
    return await handler.handle(
        ListLeadQuery(
            company_id=company_id,
            contact_id=contact_id,
            skip=skip,
            limit=limit,
        )
    )


@router.get(
    "/search",
    response_model=list[LeadResponseDTO],
)
async def search_leads(
    handler: SearchLeadHandlerDependency,
    keyword: str = Query(..., min_length=1),
    company_id: str | None = Query(default=None),
    contact_id: str | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
) -> list[LeadResponseDTO]:
    """Search Leads."""
    return await handler.handle(
        SearchLeadQuery(
            search_term=keyword,
            company_id=company_id,
            contact_id=contact_id,
            skip=skip,
            limit=limit,
        )
    )


@router.get(
    "/{lead_id}",
    response_model=LeadResponseDTO,
)
async def get_lead(
    lead_id: str,
    handler: GetLeadHandlerDependency,
) -> LeadResponseDTO:
    """Get a Lead by ID."""
    return await handler.handle(
        GetLeadQuery(lead_id=lead_id),
    )


@router.put(
    "/{lead_id}",
    response_model=LeadResponseDTO,
)
async def update_lead(
    lead_id: str,
    request: UpdateLeadRequestDTO,
    handler: UpdateLeadHandlerDependency,
) -> LeadResponseDTO:
    """Update a Lead."""
    return await handler.handle(
        LeadMapper.to_update_command(request, lead_id),
    )


@router.get(
    "/{lead_id}/review",
    response_model=LeadReviewChainResponseDTO,
)
async def get_lead_review_chain(
    lead_id: str,
    handler: GetLeadReviewChainHandlerDependency,
) -> LeadReviewChainResponseDTO:
    """Get the full evidence -> hypothesis -> recommendation chain for a Lead."""
    return await handler.handle(lead_id)


@router.get(
    "/{lead_id}/compliance-ruleset",
    response_model=LeadComplianceRulesetResponseDTO,
)
async def get_lead_compliance_ruleset(
    lead_id: str,
    handler: GetLeadComplianceRulesetHandlerDependency,
) -> LeadComplianceRulesetResponseDTO:
    """Resolve the jurisdiction-aware compliance ruleset for a Lead."""
    return await handler.handle(lead_id)


@router.post(
    "/{lead_id}/submit-for-review",
    response_model=LeadResponseDTO,
)
async def submit_lead_for_review(
    lead_id: str,
    handler: SubmitLeadForReviewHandlerDependency,
) -> LeadResponseDTO:
    """Submit a Lead for human review before any future outreach."""
    return await handler.handle(SubmitLeadForReviewCommand(lead_id=lead_id))


@router.post(
    "/{lead_id}/approve",
    response_model=LeadResponseDTO,
)
async def approve_lead(
    lead_id: str,
    handler: ApproveLeadHandlerDependency,
    request: LeadReviewDecisionRequestDTO | None = None,
) -> LeadResponseDTO:
    """Approve a pending-review Lead."""
    return await handler.handle(
        ApproveLeadCommand(lead_id=lead_id, notes=request.notes if request else None),
    )


@router.post(
    "/{lead_id}/reject",
    response_model=LeadResponseDTO,
)
async def reject_lead(
    lead_id: str,
    handler: RejectLeadHandlerDependency,
    request: LeadReviewDecisionRequestDTO | None = None,
) -> LeadResponseDTO:
    """Reject a pending-review Lead. It can be resubmitted afterward."""
    return await handler.handle(
        RejectLeadCommand(lead_id=lead_id, notes=request.notes if request else None),
    )


@router.post(
    "/{lead_id}/classify-reply",
    response_model=ReplyClassificationResponseDTO,
)
async def classify_reply(
    lead_id: str,
    request: ClassifyReplyRequestDTO,
    handler: ClassifyReplyHandlerDependency,
) -> ReplyClassificationResponseDTO:
    """Classify an inbound reply and apply it to the Lead (EPIC-10.1/10.3)."""
    return await handler.handle(
        ClassifyReplyCommand(lead_id=lead_id, reply_text=request.reply_text),
    )


@router.delete(
    "/{lead_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_lead(
    lead_id: str,
    handler: DeleteLeadHandlerDependency,
) -> Response:
    """Delete a Lead."""
    await handler.handle(
        DeleteLeadCommand(lead_id=lead_id),
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
