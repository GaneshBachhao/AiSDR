import json
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.ai.agents.research_agent import ResearchAgent
from app.common.utils.datetime_utils import utc_now
from app.core.config import settings
from app.core.logger import logger
from app.models.lead_research import LeadResearch
from app.repositories.lead_repository import LeadRepository
from app.repositories.lead_research_repository import LeadResearchRepository
from app.schemas.lead_research_schema import LeadResearchCreate

from app.knowledge.research_enrichment import ResearchEnrichment
from app.knowledge.ai_solution_catalog import CATALOG_VERSION

from app.recommendation.services.recommendation_service import RecommendationService


class ResearchService:

    def __init__(self):
        self.lead_repository = LeadRepository()
        self.research_repository = LeadResearchRepository()
        self.agent = ResearchAgent()
        self.enrichment = ResearchEnrichment()
        self.recommendation_service = RecommendationService()

    def research_lead(
        self,
        db: Session,
        lead_id: int
    ) -> LeadResearch:
        """
        Research a lead using AI and save the result.
        Returns cached research if it is still valid.
        """

        # Step 1 - Load Lead
        lead = self.lead_repository.get_by_id(
            db,
            lead_id
        )

        if not lead:
            logger.warning(f"Lead not found. Lead ID: {lead_id}")
            raise ValueError("Lead not found.")

        logger.info(
            f"Starting research for Lead ID: {lead.id} ({lead.company_name})"
        )

        # Step 2 - Check Cache
        latest = self.research_repository.get_latest(
            db,
            lead.id
        )

        if latest:

            cache_limit = utc_now() - timedelta(
                days=settings.RESEARCH_CACHE_DAYS
            )

            if latest.created_at >= cache_limit:

                logger.info(
                    f"Using cached research for Lead ID: {lead.id}"
                )

                return latest

        # Step 3 - Generate AI Research
        logger.info(
            f"Generating new AI research for Lead ID: {lead.id}"
        )

        result = self.agent.research_company(
            company_name=lead.company_name,
            website=lead.website
        )

        result = self.enrichment.enrich(result)

        # Step 4 - Prepare Database Object
        research = LeadResearchCreate(
            lead_id=lead.id,
            company_name=result["company_name"],
            industry=result.get("industry"),
            summary=result.get("summary"),
            business_model=result.get("business_model"),
            pain_points=json.dumps(result.get("pain_points", [])),
            ai_opportunities=json.dumps(result.get("ai_opportunities", [])),
            recommended_services=json.dumps(result.get("recommended_services", [])),
            decision_makers=json.dumps(result.get("decision_makers", [])),
            buying_signals=json.dumps(result.get("buying_signals", [])),
            confidence_score=result.get("confidence_score"),
            matched_sector=result.get("matched_sector"),
            sector_confidence=result.get("sector_confidence"),
            catalog_services=json.dumps(result.get("catalog_services", [])),
            generic_ai_opportunities=json.dumps(result.get("generic_ai_opportunities", [])),
            catalog_version=CATALOG_VERSION,
            model_name=settings.AI_MODEL
        )

        # Step 5 - Save Research
        saved_research = self.research_repository.create(
            db,
            research
        )

        recommendation = (
            self.recommendation_service.generate(
                enriched_research=result,
            )
        )

        self.recommendation_service.save(
            db=db,
            lead_research_id=saved_research.id,
            recommendation_response=recommendation,
        )

        logger.info(
            "Generated %d recommendation(s) for Lead ID: %s",
            len(recommendation.recommendations),
            lead.id,
        )

        logger.info(
            f"Research saved successfully for Lead ID: {lead.id}"
        )

        return saved_research