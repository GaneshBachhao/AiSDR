"""List Compliance Rulesets application handler (EPIC-11)."""

from __future__ import annotations

from app.application.compliance.compliance_mapper import ComplianceMapper
from app.application.compliance.dto.compliance_responses import (
    ComplianceRulesetResponseDTO,
)
from app.domain.compliance.value_objects.compliance_ruleset import ComplianceRuleset


class ListComplianceRulesetsHandler:
    """List every loaded compliance ruleset -- a visibility/debug endpoint,
    same spirit as GET /admin/ai-config."""

    def __init__(self, rulesets: dict[str, ComplianceRuleset]) -> None:
        self._rulesets = rulesets

    async def handle(self) -> list[ComplianceRulesetResponseDTO]:
        return [ComplianceMapper.to_response(ruleset) for ruleset in self._rulesets.values()]
