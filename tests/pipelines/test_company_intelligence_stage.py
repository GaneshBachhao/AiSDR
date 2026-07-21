"""
Tests for CompanyIntelligenceStage.
"""

import pytest

from app.company_intelligence.schemas.company_profile_schema import (
    CompanyProfile,
)

from app.lead_intelligence.schemas.lead_candidate_schema import (
    LeadCandidate,
)

from app.pipelines.context.pipeline_context import (
    PipelineContext,
)

from app.pipelines.stages.company_intelligence_stage import (
    CompanyIntelligenceStage,
)


# ==========================================================
# Fake Services
# ==========================================================


class FakeCompanyIntelligenceService:
    """
    Simulates successful enrichment.
    """

    def enrich(
        self,
        candidate: LeadCandidate,
    ) -> CompanyProfile:

        return CompanyProfile(
            company_name=candidate.company_name,
            website=str(candidate.website)
            if candidate.website
            else None,
            industry="Manufacturing",
            employee_count=250,
            country="India",
            state="Maharashtra",
            city="Pune",
        )


class FailingCompanyIntelligenceService:
    """
    Simulates enrichment failure.
    """

    def enrich(
        self,
        candidate: LeadCandidate,
    ) -> CompanyProfile:

        raise RuntimeError(
            "Gemini unavailable"
        )


# ==========================================================
# Helpers
# ==========================================================


def build_candidate() -> LeadCandidate:

    return LeadCandidate(
        company_name="ABC Manufacturing",
        website="https://abc.com",
        industry="Manufacturing",
        country="India",
        state="Maharashtra",
        city="Pune",
        source="Unit Test",
        confidence=1.0,
        metadata={},
    )


# ==========================================================
# Tests
# ==========================================================


def test_company_intelligence_success():

    context = PipelineContext(
        candidate=build_candidate(),
    )

    stage = CompanyIntelligenceStage(
        service=FakeCompanyIntelligenceService(),
    )

    result = stage.execute(context)

    assert result.company_profile is not None

    assert (
        result.company_profile.company_name
        == "ABC Manufacturing"
    )

    assert result.errors == []

    assert result.warnings == []

    assert (
        result.stage_results[
            "Company Intelligence"
        ]["success"]
        is True
    )

    assert (
        result.stage_results[
            "Company Intelligence"
        ]["fallback"]
        is False
    )


def test_company_intelligence_fallback():

    context = PipelineContext(
        candidate=build_candidate(),
    )

    stage = CompanyIntelligenceStage(
        service=FailingCompanyIntelligenceService(),
    )

    result = stage.execute(context)

    assert result.company_profile is not None

    assert (
        result.company_profile.company_name
        == "ABC Manufacturing"
    )

    assert result.errors == []

    assert len(result.warnings) == 1

    assert (
        result.stage_results[
            "Company Intelligence"
        ]["success"]
        is True
    )

    assert (
        result.stage_results[
            "Company Intelligence"
        ]["fallback"]
        is True
    )


def test_candidate_required():

    context = PipelineContext()

    stage = CompanyIntelligenceStage(
        service=FakeCompanyIntelligenceService(),
    )

    with pytest.raises(ValueError):
        stage.execute(context)