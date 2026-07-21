"""
Tests for QualificationStage.
"""

import pytest

from app.company_intelligence.schemas.company_profile_schema import (
    CompanyProfile,
)

from app.lead_intelligence.qualification.schemas.qualification_result_schema import (
    QualificationResult,
)

from app.pipelines.context.pipeline_context import (
    PipelineContext,
)

from app.pipelines.stages.qualification_stage import (
    QualificationStage,
)


# ==========================================================
# Fake Qualification Services
# ==========================================================


class FakeQualifiedService:
    """
    Always qualifies the company.
    """

    def qualify(
        self,
        company,
        icp,
    ):

        return QualificationResult(

            qualified=True,

            score=92,

            matched_rules=[
                "Industry",
                "Employee Count",
            ],

            failed_rules=[],

            recommendations=[],
        )


class FakeRejectedService:
    """
    Always rejects the company.
    """

    def qualify(
        self,
        company,
        icp,
    ):

        return QualificationResult(

            qualified=False,

            score=38,

            matched_rules=[],

            failed_rules=[
                "Industry",
            ],

            recommendations=[],
        )


# ==========================================================
# Test Helpers
# ==========================================================


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


# ==========================================================
# Tests
# ==========================================================


def test_company_qualified():

    context = PipelineContext(

        company_profile=build_company(),

    )

    stage = QualificationStage(

        qualification_service=FakeQualifiedService(),

    )

    result = stage.execute(context)

    assert result.qualification is not None

    assert result.qualification.qualified is True

    assert result.qualification.score == 92

    assert result.errors == []

    assert result.warnings == []

    assert "Qualification" in result.stage_results

    assert (
        result.stage_results["Qualification"]["qualified"]
        is True
    )

    assert (
        result.stage_results["Qualification"]["score"]
        == 92
    )

    assert (
        result.stage_results["Qualification"]["matched_rules"]
        == [
            "Industry",
            "Employee Count",
        ]
    )

    assert (
        result.stage_results["Qualification"]["failed_rules"]
        == []
    )


def test_company_rejected():

    context = PipelineContext(

        company_profile=build_company(),

    )

    stage = QualificationStage(

        qualification_service=FakeRejectedService(),

    )

    result = stage.execute(context)

    assert result.qualification is not None

    assert result.qualification.qualified is False

    assert result.qualification.score == 38

    assert result.errors == []

    assert result.warnings == []

    assert "Qualification" in result.stage_results

    assert (
        result.stage_results["Qualification"]["qualified"]
        is False
    )

    assert (
        result.stage_results["Qualification"]["score"]
        == 38
    )

    assert (
        result.stage_results["Qualification"]["matched_rules"]
        == []
    )

    assert (
        result.stage_results["Qualification"]["failed_rules"]
        == [
            "Industry",
        ]
    )


def test_company_profile_required():

    context = PipelineContext()

    stage = QualificationStage()

    with pytest.raises(ValueError):

        stage.execute(context)