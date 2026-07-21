"""
Tests for LeadCreationStage.
"""

from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from app.company_intelligence.schemas.company_profile_schema import (
    CompanyProfile,
)

from app.exceptions.custom_exceptions import (
    DuplicateLeadException,
)

from app.lead_intelligence.qualification.schemas.qualification_result_schema import (
    QualificationResult,
)

from app.models.lead import Lead

from app.pipelines.context.pipeline_context import (
    PipelineContext,
)

from app.pipelines.stages.lead_creation_stage import (
    LeadCreationStage,
)


# ==========================================================
# Fake Lead Services
# ==========================================================


class FakeLeadService:
    """
    Simulates successful lead creation.
    """

    def create_lead(
        self,
        db,
        lead,
    ):

        return Lead(

            id=1,

            company_name=lead.company_name,

            website=lead.website,

        )


class FakeDuplicateLeadService:
    """
    Simulates duplicate lead.
    """

    def create_lead(
        self,
        db,
        lead,
    ):

        raise DuplicateLeadException(
            lead.company_name,
        )


class FakeFailureLeadService:
    """
    Simulates unexpected database failure.
    """

    def create_lead(
        self,
        db,
        lead,
    ):

        raise RuntimeError(
            "Database failure"
        )


# ==========================================================
# Helpers
# ==========================================================


def build_db():

    return MagicMock(spec=Session)


def build_company():

    return CompanyProfile(

        company_name="ABC Manufacturing",

        website="https://abc.com",

        industry="Manufacturing",

        employee_count=250,

        country="India",

        state="Maharashtra",

        city="Pune",

    )


def build_qualification():

    return QualificationResult(

        qualified=True,

        score=92,

        matched_rules=[
            "Industry",
        ],

        failed_rules=[],

    )


def build_unqualified():

    return QualificationResult(

        qualified=False,

        score=40,

        matched_rules=[],

        failed_rules=[
            "Industry",
        ],

    )


# ==========================================================
# Tests
# ==========================================================


def test_lead_created_successfully():

    context = PipelineContext(

        db=build_db(),

        company_profile=build_company(),

        qualification=build_qualification(),

    )

    stage = LeadCreationStage(

        lead_service=FakeLeadService(),

    )

    result = stage.execute(context)

    assert result.lead is not None

    assert result.lead.company_name == "ABC Manufacturing"

    assert result.errors == []

    assert result.warnings == []

    assert (

        result.stage_results["Lead Creation"]["status"]

        == "SUCCESS"

    )


def test_duplicate_lead_warning():

    context = PipelineContext(

        db=build_db(),

        company_profile=build_company(),

        qualification=build_qualification(),

    )

    stage = LeadCreationStage(

        lead_service=FakeDuplicateLeadService(),

    )

    result = stage.execute(context)

    assert result.lead is None

    assert len(result.warnings) == 1

    assert result.errors == []

    assert (

        result.stage_results["Lead Creation"]["status"]

        == "WARNING"

    )


def test_database_failure():

    context = PipelineContext(

        db=build_db(),

        company_profile=build_company(),

        qualification=build_qualification(),

    )

    stage = LeadCreationStage(

        lead_service=FakeFailureLeadService(),

    )

    with pytest.raises(RuntimeError):

        stage.execute(context)

    assert len(context.errors) == 1


def test_company_profile_required():

    context = PipelineContext(

        db=build_db(),

        qualification=build_qualification(),

    )

    stage = LeadCreationStage()

    with pytest.raises(ValueError):

        stage.execute(context)


def test_database_required():

    context = PipelineContext(

        company_profile=build_company(),

        qualification=build_qualification(),

    )

    stage = LeadCreationStage()

    with pytest.raises(ValueError):

        stage.execute(context)


def test_can_execute_when_not_qualified():

    context = PipelineContext(

        company_profile=build_company(),

        qualification=build_unqualified(),

    )

    stage = LeadCreationStage()

    assert stage.can_execute(context) is False

    assert (

        context.stage_results["Lead Creation"]["status"]

        == "SKIPPED"

    )


def test_can_execute_without_qualification():

    context = PipelineContext(

        company_profile=build_company(),

    )

    stage = LeadCreationStage()

    assert stage.can_execute(context) is False


def test_can_execute_without_company():

    context = PipelineContext(

        qualification=build_qualification(),

    )

    stage = LeadCreationStage()

    assert stage.can_execute(context) is False