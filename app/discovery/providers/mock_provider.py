from app.discovery.providers.base_provider import BaseDiscoveryProvider
from app.discovery.schemas.discovery_schema import DiscoveryResult


class MockDiscoveryProvider(BaseDiscoveryProvider):
    """
    Mock provider for development and testing.
    """

    def discover(
        self,
        industry: str,
        location: str,
        max_results: int = 10
    ) -> list[DiscoveryResult]:

        companies = [
            DiscoveryResult(
                company_name="Cyclone Automotive",
                website="https://cycloneautomotive.com",
                industry=industry,
                location=location,
                source="Mock Provider"
            ),
            DiscoveryResult(
                company_name="Navitasys India",
                website="https://navitasys.com",
                industry=industry,
                location=location,
                source="Mock Provider"
            ),
            DiscoveryResult(
                company_name="NextGen Manufacturing",
                website="https://nextgenmanufacturing.com",
                industry=industry,
                location=location,
                source="Mock Provider"
            ),
            DiscoveryResult(
                company_name="Smart Retail Solutions",
                website="https://smartretail.com",
                industry=industry,
                location=location,
                source="Mock Provider"
            ),
            DiscoveryResult(
                company_name="Deccan Nutraceuticals",
                website="https://deccannutraceuticals.com",
                industry=industry,
                location=location,
                source="Mock Provider"
            ),
        ]

        return companies[:max_results]