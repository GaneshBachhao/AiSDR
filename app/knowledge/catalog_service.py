from app.knowledge.ai_solution_catalog import AI_SOLUTION_CATALOG


class CatalogService:
    """
    Service for querying the AgneticAI Solution Catalog.
    """

    def get_all_sectors(self) -> list[str]:
        """
        Return all supported sectors.
        """
        return sorted(AI_SOLUTION_CATALOG.keys())

    def get_sector(self, sector: str) -> dict | None:
        """
        Return the catalog entry for a sector.
        """
        return AI_SOLUTION_CATALOG.get(sector)

    def get_services(self, sector: str) -> list[dict]:
        """
        Return AgneticAI catalog services.
        """
        entry = self.get_sector(sector)

        if not entry:
            return []

        return entry.get("services", [])

    def get_generic_opportunities(
        self,
        sector: str,
    ) -> list[str]:
        """
        Return fallback AI opportunities.
        """
        entry = self.get_sector(sector)

        if not entry:
            return []

        return entry.get(
            "generic_opportunities",
            [],
        )

    def get_pain_points(
        self,
        sector: str,
    ) -> list[str]:
        """
        Return common pain points.
        """
        entry = self.get_sector(sector)

        if not entry:
            return []

        return entry.get(
            "pain_points",
            [],
        )

    def get_keywords(
        self,
        sector: str,
    ) -> list[str]:
        """
        Return industry keywords.
        """
        entry = self.get_sector(sector)

        if not entry:
            return []

        return entry.get(
            "keywords",
            [],
        )