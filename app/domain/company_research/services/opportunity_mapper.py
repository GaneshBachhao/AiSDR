from __future__ import annotations


class OpportunityMapper:
    """Maps detected buying signals to opportunity types and recommended services.

    Kept separate from scoring/response-assembly so both the qualification
    scorer (which needs to know whether a candidate's implied services match
    the requested ones) and the response mapper (which needs the same
    opportunity/service list for display) share one source of truth.
    """

    SERVICE_ALIASES = {
        "azure modernization": ("azure", "modernization", "migration"),
        "custom application development": ("application", "software", "development"),
        "business process automation": ("automation", "workflow", "process"),
        "ai consulting": ("ai", "artificial intelligence"),
        "architecture review": ("architecture", "modernization", "cloud"),
    }

    @classmethod
    def map_signals(cls, signals: dict[str, bool]) -> tuple[list[str], list[str]]:
        opportunities: list[str] = []
        services: list[str] = []
        if signals.get("ai"):
            opportunities.append("AI / Generative AI")
            services.append("AI Consulting")
        if signals.get("process"):
            opportunities.append("Workflow / Process Improvement")
            services.append("Business Process Automation")
        if signals.get("technology"):
            opportunities.append("Cloud / Software Modernization")
            services.extend(["Custom Application Development", "Azure Modernization", "Architecture Review"])
        if not opportunities:
            opportunities.append("Technology modernization")
            services.extend(["Architecture Review", "Custom Application Development"])
        return opportunities, list(dict.fromkeys(services))

    @classmethod
    def service_matches_requested(cls, service: str, requested: list[str]) -> bool:
        value = service.lower()
        aliases = cls.SERVICE_ALIASES.get(value, ())
        return any(
            value in requested_service.lower()
            or requested_service.lower() in value
            or any(alias in requested_service.lower() for alias in aliases)
            for requested_service in requested
        )

    @classmethod
    def any_service_matches(cls, services: list[str], requested: list[str]) -> bool:
        if not requested:
            return False
        return any(cls.service_matches_requested(service, requested) for service in services)
