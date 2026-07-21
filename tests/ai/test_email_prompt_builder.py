from app.ai.prompts.email_prompt_builder import (
    EmailPromptBuilder,
)

from app.company_intelligence.schemas.company_profile_schema import (
    CompanyProfile,
)

from app.contacts.schemas.contact_schema import (
    ContactCreate,
)

from app.recommendation.schemas.recommendation_schema import (
    RecommendationItem,
    RecommendationResponse,
)


def test_build_prompt():

    company = CompanyProfile(
        company_name="ABC Manufacturing",
        industry="Manufacturing",
        description="Industrial equipment manufacturer",
        products=["Robots"],
        services=["Maintenance"],
    )

    contact = ContactCreate(
        lead_id=1,
        full_name="John Doe",
        email="john@test.com",
        job_title="Operations Manager",
    )

    recommendations = RecommendationResponse(
        matched_sector="Manufacturing",
        sector_confidence=0.95,
        generic_ai_opportunities=[
            "Predictive maintenance"
        ],
        recommendations=[
            RecommendationItem(
                service_id="svc001",
                service_name="Predictive Maintenance",
                category="AI",
                priority="High",
                difficulty="Medium",
                roi="High",
                target_personas=[],
                deliverables=[],
                estimated_duration_weeks=6,
            )
        ],
    )

    prompt = EmailPromptBuilder.build(
        company,
        contact,
        recommendations,
    )

    assert "ABC Manufacturing" in prompt
    assert "John Doe" in prompt
    assert "Predictive Maintenance" in prompt