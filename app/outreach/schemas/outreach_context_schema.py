from pydantic import BaseModel


class OutreachContext(BaseModel):
    """
    Complete context used for AI-generated outreach.
    """

    lead_id: int

    company_name: str

    website: str | None = None

    industry: str | None = None

    summary: str | None = None

    business_model: str | None = None

    pain_points: list[str] = []

    ai_opportunities: list[str] = []

    buying_signals: list[str] = []

    decision_makers: list[str] = []

    matched_sector: str | None = None

    recommendations: list[dict] = []