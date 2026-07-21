from app.core.logger import logger
from app.knowledge.catalog_service import CatalogService
from app.knowledge.sector_matcher import SectorMatcher


class ResearchEnrichment:
    """
    Enriches AI research using AgneticAI's consulting knowledge.

    Responsibilities:
    - Match business sector
    - Recommend AgneticAI services
    - Suggest generic AI opportunities

    Supports:
    - raw research dictionaries
    - company profile objects from pipeline context
    """

    def __init__(self):
        self.catalog_service = CatalogService()
        self.sector_matcher = SectorMatcher()

    def enrich(
        self,
        research: dict | None = None,
        company_profile=None,
    ) -> dict:
        """
        Enrich research information.

        Args:
            research:
                AI generated research dictionary.

            company_profile:
                CompanyProfile schema from pipeline.

        Returns:
            Enriched research dictionary.
        """

        logger.info("=" * 60)
        logger.info("Research Enrichment Started")

        # --------------------------------------------------
        # Normalize input
        # --------------------------------------------------

        if company_profile is not None:
            research = self._convert_company_profile(
                company_profile
            )

        if research is None:
            raise ValueError(
                "Research data is required for enrichment."
            )

        # --------------------------------------------------
        # Build search text
        # --------------------------------------------------

        search_text = " ".join(
            filter(
                None,
                [
                    research.get("industry") or "",
                    research.get("summary") or "",
                    " ".join(
                        research.get(
                            "pain_points",
                            []
                        )
                        or []
                    ),
                ],
            )
        )

        # --------------------------------------------------
        # Sector matching
        # --------------------------------------------------

        match = self.sector_matcher.match(
            search_text
        )

        sector = match["sector"]
        confidence = match["confidence"]

        logger.info(
            f"Matched Sector: {sector} ({confidence:.2f})"
        )

        # --------------------------------------------------
        # Catalog enrichment
        # --------------------------------------------------

        services = (
            self.catalog_service.get_services(
                sector
            )
        )

        opportunities = (
            self.catalog_service
            .get_generic_opportunities(
                sector
            )
        )

        enriched = research.copy()

        enriched.update(
            {
                "matched_sector": sector,
                "sector_confidence": confidence,
                "catalog_services": services,
                "generic_ai_opportunities": opportunities,
            }
        )

        logger.info(
            f"Catalog Services: {len(services)}"
        )

        logger.info(
            f"Generic Opportunities: {len(opportunities)}"
        )

        logger.info(
            "Research Enrichment Completed"
        )

        logger.info("=" * 60)

        return enriched

    # ------------------------------------------------------
    # Helpers
    # ------------------------------------------------------

    def _convert_company_profile(
        self,
        company_profile,
    ) -> dict:
        """
        Convert CompanyProfile schema
        into enrichment input format.
        """

        if hasattr(
            company_profile,
            "model_dump",
        ):
            return {
                key: value
                for key, value in company_profile.model_dump().items()
                if value is not None
            }

        if isinstance(
            company_profile,
            dict,
        ):
            return company_profile

        return {
            "industry": getattr(
                company_profile,
                "industry",
                "",
            ),
            "summary": getattr(
                company_profile,
                "summary",
                "",
            ),
            "pain_points": getattr(
                company_profile,
                "pain_points",
                [],
            ),
        }
    
    