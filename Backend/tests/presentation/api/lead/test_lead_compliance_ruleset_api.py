"""Tests for GET /leads/{id}/compliance-ruleset (EPIC-11)."""

from __future__ import annotations

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.compliance.dto.compliance_responses import (
    ComplianceRulesetResponseDTO,
    LeadComplianceRulesetResponseDTO,
)
from app.application.compliance.handlers.get_lead_compliance_ruleset_handler import (
    GetLeadComplianceRulesetHandler,
)
from app.presentation.api.dependencies.handlers import (
    get_lead_compliance_ruleset_handler,
)
from app.presentation.api.exception_handlers import register_exception_handlers
from app.presentation.api.routers.lead_router import router

_LEAD_ID = str(uuid4())


@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    register_exception_handlers(app)
    return app


@pytest.fixture
def client(app):
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_resolves_and_returns_the_ruleset(app, client):
    handler = AsyncMock(spec=GetLeadComplianceRulesetHandler)
    handler.handle.return_value = LeadComplianceRulesetResponseDTO(
        lead_id=_LEAD_ID,
        company_country="United States",
        ruleset=ComplianceRulesetResponseDTO(
            jurisdiction_code="US",
            regime_name="CAN-SPAM",
            consent_model="opt-out",
            requires_unsubscribe_link=True,
            requires_physical_address=True,
            cooldown_days=None,
            notes="",
        ),
    )
    app.dependency_overrides[get_lead_compliance_ruleset_handler] = lambda: handler

    response = client.get(f"/leads/{_LEAD_ID}/compliance-ruleset")

    assert response.status_code == 200
    body = response.json()
    assert body["ruleset"]["jurisdiction_code"] == "US"
    assert body["company_country"] == "United States"


def test_not_found_returns_404(app, client):
    handler = AsyncMock(spec=GetLeadComplianceRulesetHandler)
    handler.handle.side_effect = NotFoundException(message="Lead not found.")
    app.dependency_overrides[get_lead_compliance_ruleset_handler] = lambda: handler

    response = client.get(f"/leads/{_LEAD_ID}/compliance-ruleset")

    assert response.status_code == 404
