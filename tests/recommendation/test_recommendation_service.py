from app.recommendation.services.recommendation_service import (
    RecommendationService,
)


def test_generate_recommendations():

    service = RecommendationService()

    enriched_research = {

        "matched_sector": "Manufacturing",

        "sector_confidence": 0.95,

        "catalog_services": [

            {
                "id": "proposal_generator",

                "name": "Proposal Generator",

                "category": "Document AI",

                "priority": "HIGH",

                "difficulty": "LOW",

                "roi": "Reduce proposal preparation time.",

                "target_personas": [
                    "Sales Manager"
                ],

                "deliverables": [
                    "Proposal Generator"
                ],

                "estimated_duration_weeks": 2,
            }

        ],

        "generic_ai_opportunities": [

            "Digital Twin",

            "Computer Vision"

        ],
    }

    result = service.generate(
        enriched_research
    )

    assert result.matched_sector == "Manufacturing"

    assert result.sector_confidence == 0.95

    assert len(result.recommendations) == 1

    assert (
        result.recommendations[0].service_name
        == "Proposal Generator"
    )

    assert (
        len(result.generic_ai_opportunities)
        == 2
    )