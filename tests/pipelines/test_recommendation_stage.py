from app.company_intelligence.schemas.company_profile_schema import (
    CompanyProfile,
)

from app.pipelines.context.pipeline_context import (
    PipelineContext,
)

from app.pipelines.stages.recommendation_stage import (
    RecommendationStage,
)

from app.recommendation.schemas.recommendation_schema import (
    RecommendationItem,
    RecommendationResponse,
)


class FakeEnrichment:

    def enrich(
        self,
        company_profile,
    ):

        return {

            "matched_sector": "Manufacturing",

            "sector_confidence": 0.95,

            "catalog_services": [

                {

                    "id": "svc001",

                    "name": "Predictive Maintenance",

                    "category": "AI",

                    "priority": "High",

                    "difficulty": "Medium",

                    "roi": "High",

                }

            ],

            "generic_ai_opportunities": [],
        }


class FakeRecommendationService:

    def generate(
        self,
        enriched,
    ):

        return RecommendationResponse(

            matched_sector="Manufacturing",

            sector_confidence=0.95,

            generic_ai_opportunities=[],

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


def test_recommendation_stage():

    stage = RecommendationStage()

    stage.enrichment = FakeEnrichment()

    stage.service = FakeRecommendationService()

    context = PipelineContext()

    context.company_profile = CompanyProfile(

        company_name="ABC Manufacturing",

    )

    result = stage.execute(
        context,
    )

    assert result.recommendations is not None

    assert len(
        result.recommendations.recommendations
    ) == 1

    assert (

        result.recommendations.recommendations[0].service_name

        == "Predictive Maintenance"

    )


def test_can_execute():

    stage = RecommendationStage()

    context = PipelineContext()

    assert stage.can_execute(context) is False

    context.company_profile = CompanyProfile(

        company_name="ABC",

    )

    assert stage.can_execute(context) is True