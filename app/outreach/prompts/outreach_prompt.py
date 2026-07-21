import json

from app.outreach.schemas.outreach_context_schema import (
    OutreachContext,
)


def build_outreach_prompt(
    context: OutreachContext,
) -> str:
    """
    Builds the prompt used to generate
    a personalized outreach kit.
    """

    recommendations = json.dumps(
        context.recommendations,
        indent=2,
    )

    prompt = f"""
You are a senior AI Consulting Business Development Manager.

Your objective is to prepare a highly personalized outreach kit
for a prospective client.

The communication must:

- Be professional.
- Never oversell.
- Never invent facts.
- Reference only the supplied business context.
- Demonstrate understanding of the company's industry.
- Focus on business outcomes instead of AI technology.
- Encourage a discovery meeting.
- Keep every communication concise.

--------------------------------------------------
COMPANY INFORMATION
--------------------------------------------------

Company:
{context.company_name}

Website:
{context.website}

Industry:
{context.industry}

Business Summary:
{context.summary}

Business Model:
{context.business_model}

--------------------------------------------------
IDENTIFIED PAIN POINTS
--------------------------------------------------

{json.dumps(context.pain_points, indent=2)}

--------------------------------------------------
AI OPPORTUNITIES
--------------------------------------------------

{json.dumps(context.ai_opportunities, indent=2)}

--------------------------------------------------
BUYING SIGNALS
--------------------------------------------------

{json.dumps(context.buying_signals, indent=2)}

--------------------------------------------------
DECISION MAKERS
--------------------------------------------------

{json.dumps(context.decision_makers, indent=2)}

--------------------------------------------------
RECOMMENDED AGNETICAI SERVICES
--------------------------------------------------

{recommendations}

--------------------------------------------------
GENERATE
--------------------------------------------------

Generate:

1. Professional Email
2. LinkedIn Connection Message
3. WhatsApp Intro Message
4. Cold Call Opening Script
5. Discovery Meeting Objective

The tone should be:

Professional

Consultative

Helpful

Non-salesy

Natural

--------------------------------------------------
IMPORTANT
--------------------------------------------------

Do NOT make unrealistic promises.

Do NOT guarantee ROI.

Do NOT mention technologies unless relevant.

Never fabricate company information.

Always end with a clear call-to-action.

--------------------------------------------------
OUTPUT
--------------------------------------------------

Return ONLY valid JSON.

No markdown.

No explanations.

No code block.
"""

    return prompt