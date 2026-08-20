"""Tests for GetLeadComplianceRulesetHandler (EPIC-11)."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.compliance.handlers.get_lead_compliance_ruleset_handler import (
    GetLeadComplianceRulesetHandler,
)
from app.domain.company.entities.company import Company
from app.domain.company.identifiers.company_id import CompanyId
from app.domain.compliance.services.jurisdiction_resolver import JurisdictionResolver
from app.domain.compliance.value_objects.compliance_ruleset import ComplianceRuleset
from app.domain.contact.identifiers.contact_id import ContactId
from app.domain.lead.entities.lead import Lead


def _rulesets() -> dict[str, ComplianceRuleset]:
    return {
        "US": ComplianceRuleset(jurisdiction_code="US", regime_name="CAN-SPAM", consent_model="opt-out"),
        "DEFAULT": ComplianceRuleset(
            jurisdiction_code="DEFAULT", regime_name="Unclassified", consent_model="opt-in"
        ),
    }


@pytest.fixture
def unit_of_work():
    uow = AsyncMock()
    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = False
    return uow


@pytest.fixture
def handler(unit_of_work):
    return GetLeadComplianceRulesetHandler(
        unit_of_work=unit_of_work,
        jurisdiction_resolver=JurisdictionResolver(_rulesets()),
    )


@pytest.mark.asyncio
async def test_resolves_the_ruleset_from_the_leads_company_country(handler, unit_of_work):
    lead = Lead(company_id=CompanyId(), contact_id=ContactId())
    company = Company(name="Acme", country="United States")
    unit_of_work.lead_repository.get_by_id.return_value = lead
    unit_of_work.company_repository.get_by_id.return_value = company

    result = await handler.handle(lead.id.value)

    assert result.ruleset.jurisdiction_code == "US"
    assert result.company_country == "United States"


@pytest.mark.asyncio
async def test_falls_back_to_default_when_company_has_no_country(handler, unit_of_work):
    lead = Lead(company_id=CompanyId(), contact_id=ContactId())
    company = Company(name="Acme", country=None)
    unit_of_work.lead_repository.get_by_id.return_value = lead
    unit_of_work.company_repository.get_by_id.return_value = company

    result = await handler.handle(lead.id.value)

    assert result.ruleset.jurisdiction_code == "DEFAULT"


@pytest.mark.asyncio
async def test_raises_not_found_for_an_unknown_lead(handler, unit_of_work):
    unit_of_work.lead_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundException):
        await handler.handle(CompanyId().value)
