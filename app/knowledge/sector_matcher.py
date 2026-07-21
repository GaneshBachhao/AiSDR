from app.knowledge.catalog_service import CatalogService


class SectorMatcher:
    """
    Matches a company to the most appropriate sector
    using catalog keywords.
    """

    def __init__(self):
        self.catalog = CatalogService()

    def match(
        self,
        text: str,
    ) -> dict:
        """
        Match a company description to a catalog sector.

        Returns:
        {
            "sector": "...",
            "confidence": 95
        }
        """

        text = (text or "").lower()

        best_sector = None
        best_score = 0

        for sector in self.catalog.get_all_sectors():

            keywords = self.catalog.get_keywords(sector)

            score = sum(
                1
                for keyword in keywords
                if keyword.lower() in text
            )

            if score > best_score:
                best_score = score
                best_sector = sector

        if not best_sector:
            return {
                "sector": "Unknown",
                "confidence": 0,
            }

        confidence = min(
            100,
            best_score * 25,
        )

        return {
            "sector": best_sector,
            "confidence": confidence,
        }