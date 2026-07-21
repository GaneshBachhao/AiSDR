"""
Reply Analysis Prompt Builder
"""

from app.company_intelligence.schemas.company_profile_schema import (
    CompanyProfile,
)


class ReplyAnalysisPromptBuilder:
    """
    Builds prompts for reply analysis.
    """

    @staticmethod
    def build(
        company: CompanyProfile,
        original_email: str,
        reply: str,
    ) -> str:

        return f"""
You are an expert AI Sales Development Representative.

Analyze the customer's reply.

Company:
{company.company_name}

Industry:
{company.industry}

Original Email:
{original_email}

Customer Reply:
{reply}

Determine:

1. Customer intent
2. Overall sentiment
3. Confidence (0-1)
4. Did they request a meeting?
5. Is a follow-up needed?
6. Short reason

Allowed intents:

INTERESTED
NOT_INTERESTED
MEETING_REQUEST
NEEDS_INFORMATION
FOLLOW_UP_LATER
OUT_OF_OFFICE
ALREADY_USING_AI
ALREADY_CUSTOMER
UNKNOWN

Allowed sentiments:

POSITIVE
NEUTRAL
NEGATIVE

Return ONLY valid JSON.

{{
    "intent":"",
    "sentiment":"",
    "confidence":0.0,
    "meeting_requested":false,
    "needs_followup":false,
    "reason":""
}}
"""