"""Compliance Application Mapper."""

from __future__ import annotations

from app.application.compliance.dto.compliance_responses import (
    ComplianceRulesetResponseDTO,
)
from app.domain.compliance.value_objects.compliance_ruleset import ComplianceRuleset


class ComplianceMapper:
    """Maps Compliance domain value objects to response DTOs."""

    @staticmethod
    def to_response(ruleset: ComplianceRuleset) -> ComplianceRulesetResponseDTO:
        return ComplianceRulesetResponseDTO(
            jurisdiction_code=ruleset.jurisdiction_code,
            regime_name=ruleset.regime_name,
            consent_model=ruleset.consent_model,
            requires_unsubscribe_link=ruleset.requires_unsubscribe_link,
            requires_physical_address=ruleset.requires_physical_address,
            cooldown_days=ruleset.cooldown_days,
            notes=ruleset.notes,
        )
