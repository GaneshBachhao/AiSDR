from app.ai.schemas.generated_email_schema import (
    GeneratedEmail,
)

from app.company_intelligence.schemas.company_profile_schema import (
    CompanyProfile,
)

from app.pipelines.context.pipeline_context import (
    PipelineContext,
)

from app.pipelines.stages.ai_email_generation_stage import (
    AIEmailGenerationStage,
)

from app.recommendation.schemas.recommendation_schema import (
    RecommendationResponse,
)


class FakeContact:

    full_name = "John Doe"

    email = "john@test.com"


class FakeEmailService:

    def generate(
        self,
        company,
        contact,
        recommendations,
    ):

        return GeneratedEmail(

            subject="AI for Manufacturing",

            body="Hello John,\nLet's discuss AI.",

        )


def test_generate_email():

    stage = AIEmailGenerationStage()

    stage.service = FakeEmailService()

    context = PipelineContext()

    context.company_profile = CompanyProfile(

        company_name="ABC Manufacturing",

    )

    context.primary_contact = FakeContact()

    context.recommendations = RecommendationResponse(

        matched_sector="Manufacturing",

        sector_confidence=0.95,

        recommendations=[],

        generic_ai_opportunities=[],

    )

    result = stage.execute(
        context,
    )

    assert result.generated_email is not None

    assert (
        result.generated_email.subject
        == "AI for Manufacturing"
    )


def test_can_execute():

    stage = AIEmailGenerationStage()

    context = PipelineContext()

    assert stage.can_execute(context) is False

    context.company_profile = CompanyProfile(
        company_name="ABC",
    )

    context.primary_contact = FakeContact()

    context.recommendations = RecommendationResponse(

        matched_sector="Manufacturing",

        sector_confidence=0.95,

        recommendations=[],

        generic_ai_opportunities=[],

    )

    assert stage.can_execute(context) is True