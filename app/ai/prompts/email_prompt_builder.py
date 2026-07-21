"""
Email Prompt Builder
"""

from app.company_intelligence.schemas.company_profile_schema import (
    CompanyProfile,
)

from app.contacts.schemas.contact_schema import (
    ContactCreate,
)

from app.recommendation.schemas.recommendation_schema import (
    RecommendationResponse,
)


class EmailPromptBuilder:
    """
    Builds prompts for AI email generation.
    """

    @staticmethod
    def build(
        company: CompanyProfile,
        contact: ContactCreate,
        recommendations: RecommendationResponse,
    ) -> str:

        services = "\n".join(
            f"- {item.service_name}"
            for item in recommendations.recommendations
        )

        opportunities = "\n".join(
            recommendations.generic_ai_opportunities
        )

        return f"""
You are an expert AI Sales Development Representative.

Write a personalized cold outreach email.

Company

Name:
{company.company_name}

Industry:
{company.industry}

Description:
{company.description}

Products:
{", ".join(company.products)}

Services:
{", ".join(company.services)}

AI Opportunities

{opportunities}

Recommended Services

{services}

Recipient

Name:
{contact.full_name}

Job Title:
{contact.job_title}

Instructions

Generate:

Subject:
<subject>

Body:
<body>

Rules:

- Professional
- Friendly
- Under 200 words
- One clear CTA
- No exaggerated marketing language
- Do not invent facts
"""