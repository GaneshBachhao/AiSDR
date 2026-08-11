import importlib

company_research_router = importlib.import_module(
    "app.presentation.api.routers.company_research_router"
)
from app.presentation.main import app


class FakeResearchService:
    def search(self, request):
        return [
            {
                "company_name": "Example Manufacturing",
                "industry": "Manufacturing",
                "location": request.geography,
                "website": "https://example.com",
                "company_size": "MID_MARKET",
                "business_description": "Example manufacturing company.",
                "opportunity_type": ["Cloud / Software Modernization"],
                "evidence_of_need": "Public sources show a technology hiring signal.",
                "evidence_classification": "Strong opportunity signal",
                "business_problem_hypothesis": "The company may benefit from reviewing workflow and technology integration.",
                "recommended_solution": ["Custom Application Development"],
                "expected_business_impact": "Potentially less manual work and easier scaling.",
                "trigger_event": "Technology hiring signal",
                "evidence_date": None,
                "decision_maker_role": "CTO",
                "decision_maker_name": None,
                "public_contact_channel": "https://example.com",
                "qualification_score": 62,
                "priority_tier": "Tier B",
                "recommended_outreach_angle": "A focused technology review may be useful.",
                "suggested_first_message": "Subject: Technology improvement opportunity\n\nHello, I noticed a recent technology hiring signal and wanted to share a practical idea.",
                "sources": [],
                "confidence_level": "Medium",
                "source": "public_web_research",
            }
        ]


def test_company_research_route_is_registered_in_openapi():
    paths = app.openapi()["paths"]
    assert "/company-research/search" in paths
    assert "post" in paths["/company-research/search"]


import asyncio


def test_company_research_endpoint_returns_structured_result(monkeypatch):
    monkeypatch.setattr(company_research_router, "CompanyResearchService", FakeResearchService)

    payload = {
        "industries": ["Manufacturing"],
        "geography": "India",
        "company_size": ["MID_MARKET"],
        "technologies": ["Azure", ".NET"],
        "services": ["Custom Application Development", "Azure Modernization"],
        "number_of_companies": 1,
        "minimum_qualification_score": 60,
        "preferred_decision_makers": ["CTO"],
    }

    request = company_research_router.CompanyResearchRequest.model_validate(payload)
    body = asyncio.run(company_research_router.search_companies(request))
    assert len(body) == 1
    assert body[0]["company_name"] == "Example Manufacturing"
    assert body[0]["qualification_score"] == 62
