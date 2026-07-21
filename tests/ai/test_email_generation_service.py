from app.ai.services.email_generation_service import (
    EmailGenerationService,
)

from app.company_intelligence.schemas.company_profile_schema import (
    CompanyProfile,
)

from app.contacts.schemas.contact_schema import (
    ContactCreate,
)

from app.integrations.llm.response import (
    LLMResponse,
)

from app.recommendation.schemas.recommendation_schema import (
    RecommendationItem,
    RecommendationResponse,
)


class FakeLLM:

    def generate(
        self,
        prompt,
        temperature=None,
        max_tokens=None,
    ):

        return LLMResponse(

            text="""
Subject: AI Automation for Manufacturing

Body:

Hi John,

I'd love to discuss how AI can improve your manufacturing operations.

Best regards,
Ganesh
""",

            provider="fake",

            model="fake",

            latency_ms=1,
        )


def test_generate_email():

    service = EmailGenerationService(
        llm=FakeLLM(),
    )

    company = CompanyProfile(
        company_name="ABC Manufacturing",
    )

    contact = ContactCreate(
        lead_id=1,
        full_name="John Doe",
        email="john@test.com",
    )

    recommendations = RecommendationResponse(
        matched_sector="Manufacturing",
        sector_confidence=1,
        recommendations=[
            RecommendationItem(
                service_id="svc001",
                service_name="AI Automation",
                category="AI",
                priority="High",
                difficulty="Medium",
                roi="High",
                target_personas=[],
                deliverables=[],
                estimated_duration_weeks=6,
            )
        ],
        generic_ai_opportunities=[],
    )

    email = service.generate(
        company,
        contact,
        recommendations,
    )

    assert email.subject == "AI Automation for Manufacturing"

    assert "Hi John" in email.body