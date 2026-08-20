"""
Compliance API router (EPIC-11).

Lists the loaded jurisdiction rulesets -- a visibility/debug endpoint,
same spirit as GET /admin/ai-config. The Lead-specific resolution lives
on lead_router.py as GET /leads/{id}/compliance-ruleset instead, co-located
with EPIC-16's GET /leads/{id}/review as a lead sub-resource.
"""

from __future__ import annotations

from fastapi import APIRouter

from app.application.compliance.dto.compliance_responses import (
    ComplianceRulesetResponseDTO,
)
from app.presentation.api.dependencies.handlers import (
    ListComplianceRulesetsHandlerDependency,
)

router = APIRouter(
    prefix="/compliance",
    tags=["Compliance"],
)


@router.get(
    "/rulesets",
    response_model=list[ComplianceRulesetResponseDTO],
)
async def list_compliance_rulesets(
    handler: ListComplianceRulesetsHandlerDependency,
) -> list[ComplianceRulesetResponseDTO]:
    """List every loaded compliance ruleset."""
    return await handler.handle()
