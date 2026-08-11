from app.company_research.providers.tavily_provider import TavilyCompanyResearchProvider
from app.company_research.schemas.company_research import CompanyResearchRequest


class FakeTavilyClient:
    def search(self, query, max_results=10, search_depth="advanced"):
        if "Bad Software" in query:
            return [
                {
                    "url": "https://badsoftware.example/",
                    "title": "Bad Software - AI and IT Services",
                    "content": "Bad Software is a software development and IT services company providing SaaS and cloud consulting.",
                }
            ]
        return [
            {
                "url": "https://acme.example/",
                "title": "Acme Manufacturing",
                "content": (
                    "Acme Manufacturing is an industrial machinery manufacturer headquartered in Pune, India. "
                    "The company has 120 employees, operates production facilities and is hiring engineering staff."
                ),
                "published_date": "2026-07-01",
            }
        ]


def test_manufacturing_filter_rejects_it_company(monkeypatch):
    provider = TavilyCompanyResearchProvider()
    provider.client = FakeTavilyClient()
    request = CompanyResearchRequest(
        industries=["Manufacturing"],
        geography="India",
        number_of_companies=1,
    )
    candidate = {
        "company_name": "Bad Software",
        "website": "https://badsoftware.example",
        "title": "Bad Software",
        "content": "Bad Software is an IT services company.",
        "url": "https://badsoftware.example/",
    }
    assert provider._research_candidate(candidate, request) is None


def test_manufacturing_candidate_keeps_actual_industry_and_evidence_date():
    provider = TavilyCompanyResearchProvider()
    provider.client = FakeTavilyClient()
    request = CompanyResearchRequest(
        industries=["Manufacturing"],
        geography="India",
        number_of_companies=1,
        preferred_decision_makers=["CTO", "COO"],
    )
    candidate = {
        "company_name": "Acme Manufacturing",
        "website": "https://acme.example",
        "title": "Acme Manufacturing",
        "content": "Industrial machinery manufacturer with 120 employees.",
        "url": "https://acme.example/",
    }
    result = provider._research_candidate(candidate, request)
    assert result is not None
    assert result.industry == "Manufacturing"
    assert result.industry_match is True
    assert result.evidence_date == "2026-07-01"
    assert result.location == "Pune, India"


def test_directory_result_is_used_for_candidate_expansion_not_returned_as_company():
    provider = TavilyCompanyResearchProvider()
    content = """AVIRATA DEFENCE SYSTEMS LIMITED\n\nCountry:\n\nBengaluru, Karnataka\n\nIndia\n\nSALES REVENUE ($M)\n\n:\n\nLARSEN AND TOUBRO LIMITED\n\nCountry:\n\nMumbai, Maharashtra\n\nIndia\n\nSALES REVENUE ($M)\n\n:$16,765.98M"""
    metadata = provider._discovery_metadata(
        "Manufacturing companies in India — 13,284,167 Records",
        "https://example.com/manufacturing",
        content,
    )
    assert metadata is not None
    assert metadata["discovered_record_count"] == 13284167
    assert metadata["source_title"] == "Manufacturing companies in India — 13,284,167 Records"

    candidates = provider._extract_directory_candidates(content, "India")
    assert [item["company_name"] for item in candidates] == [
        "AVIRATA DEFENCE SYSTEMS LIMITED",
        "LARSEN AND TOUBRO LIMITED",
    ]
    assert provider._invalid_candidate_name("Find Manufacturing companies in India") is True


def test_size_gate_rejects_large_manufacturer_before_deep_research():
    provider = TavilyCompanyResearchProvider()
    provider.client = FakeTavilyClient()
    request = CompanyResearchRequest(
        industries=["Manufacturing"],
        geography="India",
        company_size=["51-200", "201-500"],
        number_of_companies=1,
    )
    candidate = {
        "company_name": "Large Steel",
        "website": "https://largesteel.example",
        "title": "Large Steel",
        "content": "Large Steel is a steel manufacturer.",
        "url": "https://largesteel.example/",
    }

    class SizeClient(FakeTavilyClient):
        def search(self, query, max_results=10, search_depth="advanced"):
            if "Large Steel" in query:
                return [{
                    "url": "https://largesteel.example/",
                    "title": "Large Steel",
                    "content": "Large Steel is a steel manufacturer headquartered in Mumbai, India with 4,916 employees.",
                }]
            return super().search(query, max_results, search_depth)

    provider.client = SizeClient()
    assert provider._research_candidate(candidate, request) is None


def test_size_gate_rejects_unknown_employee_count():
    provider = TavilyCompanyResearchProvider()
    provider.client = FakeTavilyClient()
    request = CompanyResearchRequest(
        industries=["Manufacturing"],
        geography="India",
        company_size=["51-200", "201-500"],
        number_of_companies=1,
    )
    candidate = {
        "company_name": "Unknown Size Manufacturing",
        "website": "https://unknown.example",
        "title": "Unknown Size Manufacturing",
        "content": "Industrial machinery manufacturer headquartered in Pune, India.",
        "url": "https://unknown.example/",
    }

    class UnknownClient(FakeTavilyClient):
        def search(self, query, max_results=10, search_depth="advanced"):
            if "Unknown Size Manufacturing" in query:
                return [{
                    "url": "https://unknown.example/",
                    "title": "Unknown Size Manufacturing",
                    "content": "Unknown Size Manufacturing is an industrial machinery manufacturer headquartered in Pune, India.",
                }]
            return super().search(query, max_results, search_depth)

    provider.client = UnknownClient()
    assert provider._research_candidate(candidate, request) is None
