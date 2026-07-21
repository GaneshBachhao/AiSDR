from app.knowledge.research_enrichment import ResearchEnrichment


def test_research_enrichment():

    enrichment = ResearchEnrichment()

    research = {
        "industry": "Industrial Manufacturing",
        "summary": (
            "Factory producing industrial machinery."
        ),
        "pain_points": [
            "Manual documentation",
            "Machine downtime",
        ],
    }

    result = enrichment.enrich(research)

    assert result["matched_sector"] == "Manufacturing"

    assert len(result["catalog_services"]) > 0

    assert len(result["generic_ai_opportunities"]) > 0

    assert "sector_confidence" in result

    