import json

from sqlalchemy.orm import Session

from app.models.lead_research import LeadResearch

from app.outreach.models.outreach import Outreach

from app.outreach.repositories.outreach_repository import (
    OutreachRepository,
)

from app.outreach.schemas.outreach_context_schema import (
    OutreachContext,
)

from app.outreach.schemas.outreach_schema import (
    OutreachCreate,
)

from app.repositories.lead_repository import LeadRepository
from app.repositories.lead_research_repository import (
    LeadResearchRepository,
)

from app.recommendation.models.recommendation import (
    Recommendation,
)

from app.recommendation.repositories.recommendation_repository import (
    RecommendationRepository,
)


class OutreachService:
    """
    Builds outreach context,
    generates outreach via AI,
    and persists the results.
    """

    def __init__(self):

        self.lead_repository = LeadRepository()

        self.research_repository = LeadResearchRepository()

        self.recommendation_repository = (
            RecommendationRepository()
        )

        self.outreach_repository = (
            OutreachRepository()
        )

    def build_context(
        self,
        db: Session,
        lead_id: int,
    ) -> OutreachContext:

        lead = self.lead_repository.get_by_id(
            db,
            lead_id,
        )

        if not lead:
            raise ValueError(
                "Lead not found."
            )

        research: LeadResearch | None = (
            self.research_repository.get_latest(
                db,
                lead_id,
            )
        )

        if not research:
            raise ValueError(
                "Research not found."
            )

        recommendations: list[Recommendation] = (
            self.recommendation_repository.get_by_research(
                db,
                research.id,
            )
        )

        return OutreachContext(

            lead_id=lead.id,

            company_name=lead.company_name,

            website=lead.website,

            industry=research.industry,

            summary=research.summary,

            business_model=research.business_model,

            pain_points=json.loads(
                research.pain_points or "[]"
            ),

            ai_opportunities=json.loads(
                research.ai_opportunities or "[]"
            ),

            buying_signals=json.loads(
                research.buying_signals or "[]"
            ),

            decision_makers=json.loads(
                research.decision_makers or "[]"
            ),

            matched_sector=research.matched_sector,

            recommendations=[
                {
                    "service_name": r.service_name,
                    "category": r.category,
                    "priority": r.priority,
                    "roi": r.roi,
                }
                for r in recommendations
            ],
        )

    def save(
        self,
        db: Session,
        outreach: OutreachCreate,
    ) -> Outreach:

        return self.outreach_repository.create(
            db,
            outreach,
        )