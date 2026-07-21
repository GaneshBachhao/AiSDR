from app.discovery.schemas.discovery_schema import DiscoveryRequest
from app.lead_intelligence.qualification.schemas.icp_schema import (
    IdealCustomerProfile,
)


class ICPFactory:

    @staticmethod
    def default() -> IdealCustomerProfile:
        """
        Default ICP used when no DiscoveryRequest
        is available.
        """

        return IdealCustomerProfile(
            industries=["Manufacturing"],
            locations=["India"],
            employee_min=50,
            employee_max=500,
            include_keywords=[
                "factory",
                "manufacturing",
                "industrial",
                "production",
                "plant",
                "engineering",
            ],
            exclude_keywords=[
                "software",
                "consulting",
                "it services",
                "saas",
            ],
            require_official_website=True,
            passing_score=70,
        )

    @staticmethod
    def from_request(
        request: DiscoveryRequest | None,
    ) -> IdealCustomerProfile:
        """
        Build an ICP from a DiscoveryRequest.
        Falls back to the default ICP when no
        request is supplied.
        """

        if request is None:
            return ICPFactory.default()

        return IdealCustomerProfile(
            industries=[request.industry],
            locations=[request.location],
            employee_min=50,
            employee_max=500,
            include_keywords=[
                "factory",
                "manufacturing",
                "industrial",
                "production",
                "plant",
                "engineering",
            ],
            exclude_keywords=[
                "software",
                "consulting",
                "it services",
                "saas",
            ],
            require_official_website=True,
            passing_score=70,
        )