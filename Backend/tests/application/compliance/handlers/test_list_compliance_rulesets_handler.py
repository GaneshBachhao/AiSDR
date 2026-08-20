"""Tests for ListComplianceRulesetsHandler (EPIC-11)."""

from __future__ import annotations

import pytest

from app.application.compliance.handlers.list_compliance_rulesets_handler import (
    ListComplianceRulesetsHandler,
)
from app.domain.compliance.value_objects.compliance_ruleset import ComplianceRuleset


@pytest.mark.asyncio
async def test_lists_every_loaded_ruleset() -> None:
    rulesets = {
        "US": ComplianceRuleset(jurisdiction_code="US", regime_name="CAN-SPAM"),
        "EU": ComplianceRuleset(jurisdiction_code="EU", regime_name="GDPR"),
    }
    handler = ListComplianceRulesetsHandler(rulesets)

    result = await handler.handle()

    assert {r.jurisdiction_code for r in result} == {"US", "EU"}
