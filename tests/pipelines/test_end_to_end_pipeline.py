"""
End-to-end SDR pipeline test.
"""

from unittest import result

from app.pipelines.context.pipeline_context import PipelineContext
from app.pipelines.orchestrator import PipelineOrchestrator

from app.lead_intelligence.schemas.lead_candidate_schema import (
    LeadCandidate,
)

from app.pipelines.stages.lead_creation_stage import LeadCreationStage
from app.pipelines.stages.company_intelligence_stage import (
    CompanyIntelligenceStage,
)
from app.pipelines.stages.contact_discovery_stage import (
    ContactDiscoveryStage,
)
from app.pipelines.stages.qualification_stage import (
    QualificationStage,
)
from app.pipelines.stages.recommendation_stage import (
    RecommendationStage,
)
from app.pipelines.stages.ai_email_generation_stage import (
    AIEmailGenerationStage,
)
from app.pipelines.stages.email_dispatch_stage import (
    EmailDispatchStage,
)
from tests.conftest import db_session


def test_end_to_end_sales_development_pipeline():

    candidate = LeadCandidate(
        company_name="OpenAI",
        website="https://openai.com",
        industry="Artificial Intelligence",
        country="United States",
        city="San Francisco",
        phone="+14155552671",
        email="sam@example.com",
        employee_count=5000,
        source="manual_test",
        confidence=1.0,
    )

    context = PipelineContext(
        candidate=candidate,
        db=db_session,
    )

    orchestrator = PipelineOrchestrator(
        stages=[
            CompanyIntelligenceStage(),
            QualificationStage(),
            LeadCreationStage(),
            ContactDiscoveryStage(),
            RecommendationStage(),
            AIEmailGenerationStage(),
            EmailDispatchStage(),
        ]
    )

    result = orchestrator.execute(
        context
    )

    assert result is not None

    assert result.status == "COMPLETED"

    assert result.completed_stages == [
        "Company Intelligence",
        "Qualification",
        "Recommendation",
    ]

    assert result.lead is not None

    assert result.status == "COMPLETED"

    assert result.company_profile is not None

    assert result.qualification is not None

    assert result.qualification.qualified is True

    assert result.lead is not None