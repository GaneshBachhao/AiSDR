"""
Company Intelligence Prompt Builder
"""

from app.lead_intelligence.schemas.lead_candidate_schema import (
    LeadCandidate,
)


class EnrichmentPrompt:
    """
    Builds prompts for Company Intelligence extraction.
    """

    @staticmethod
    def build(
        candidate: LeadCandidate,
    ) -> str:

        return f"""
You are an expert B2B Company Intelligence Analyst.

Your task is to enrich the following company.

Company Name:
{candidate.company_name}

Website:
{candidate.website}

Known Industry:
{candidate.industry}

Known Location:
City: {candidate.city}
State: {candidate.state}
Country: {candidate.country}

Return ONLY valid JSON.

Do NOT explain.

Do NOT use markdown.

If information is unavailable, use null.

Schema:

{{
    "company_name": "",
    "website": "",
    "linkedin_url": "",

    "country": "",
    "state": "",
    "city": "",

    "industry": "",
    "description": "",

    "employee_count": null,
    "estimated_revenue": "",

    "products": [],
    "services": [],
    "technologies": [],
    "certifications": [],

    "ai_readiness": "",
    "confidence": 0.0
}}
"""