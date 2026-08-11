from app.company_research.providers.base_provider import CompanyResearchProvider
from app.company_research.schemas.company_research import CompanyResearchRequest, CompanySearchResult
from app.company_research.services.company_research_service import CompanyResearchService


class FakeProvider(CompanyResearchProvider):
    def discover(self, request):
        return [
            CompanySearchResult(
                company_name="Example Systems",
                industry="IT",
                location=request.geography,
                website="https://example.com",
                evidence_of_need="Public sources show signals related to hiring.",
                evidence_classification="Strong opportunity signal",
                business_problem_hypothesis="The company may benefit from reviewing its technology workflow.",
                recommended_solution=["Custom Application Development"],
                expected_business_impact="Potentially less manual work and easier scaling.",
                opportunity_type=["Cloud / Software Modernization"],
                qualification_score=62,
                priority_tier="Tier B",
                recommended_outreach_angle="A focused technology review may be useful.",
                suggested_first_message="Subject: Technology improvement opportunity\n\nHello, I noticed a recent technology hiring signal and wanted to share a practical idea.",
                confidence_level="Medium",
                sources=[],
            )
        ]


def test_company_research_service_isolated_from_crm():
    request = CompanyResearchRequest(
        geography="India",
        industries=["IT"],
        number_of_companies=1,
    )
    result = CompanyResearchService(FakeProvider()).search(request)
    assert len(result) == 1
    assert result[0].company_name == "Example Systems"
    assert result[0].qualification_score == 62


def test_company_research_request_keeps_research_controls():
    request = CompanyResearchRequest(
        geography="India",
        industries=["Manufacturing"],
        company_size=["SMB"],
        technologies=["Azure", ".NET"],
        services=["Custom Application Development", "Azure Modernization"],
        ideal_customer_profile="Established manufacturers modernizing operations",
        research_period="last 6 months",
        preferred_decision_makers=["CTO", "COO"],
        number_of_companies=5,
        minimum_qualification_score=60,
    )
    assert request.research_period == "last 6 months"
    assert request.services[0] == "Custom Application Development"
    assert request.minimum_qualification_score == 60
