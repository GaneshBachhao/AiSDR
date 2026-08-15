from __future__ import annotations

from app.domain.recommendation.value_objects.solution_catalog_entry import (
    SolutionCatalogEntry,
)


class OpportunityMapper:
    """Maps detected buying signals to opportunity types and recommended services.

    Kept separate from scoring/response-assembly so both the qualification
    scorer (which needs to know whether a candidate's implied services match
    the requested ones) and the response mapper (which needs the same
    opportunity/service list for display) share one source of truth.

    ``map_signals`` reads from the shared AI Solution Catalog (see
    ``app.infrastructure.configuration.solution_catalog``) instead of its own
    hardcoded list -- "one catalog, not two" (Track 1 Phase 4 story 4.3).
    ``_DEFAULT_CATALOG`` below is a same-content fallback used only when no
    catalog is injected, so existing callers/tests remain regression-safe;
    it is not a second source of truth -- its five entries mirror
    ``general.json`` exactly, the same relationship ``IndustryClassifier``'s
    hardcoded defaults have with the seeded ``DomainProfile`` data (Track 1
    Phase 0).
    """

    SERVICE_ALIASES = {
        "azure modernization": ("azure", "modernization", "migration"),
        "custom application development": ("application", "software", "development"),
        "business process automation": ("automation", "workflow", "process"),
        "ai consulting": ("ai", "artificial intelligence"),
        "architecture review": ("architecture", "modernization", "cloud"),
    }

    _DEFAULT_CATALOG: tuple[SolutionCatalogEntry, ...] = (
        SolutionCatalogEntry(
            id="ai-consulting", sector="general", pain_point="AI / Generative AI",
            solution_type="AI Agent", title="AI Consulting",
            description="Advisory and delivery for adopting generative AI and automation.",
            is_existing_offering=True, signals=("ai",),
        ),
        SolutionCatalogEntry(
            id="business-process-automation", sector="general",
            pain_point="Workflow / Process Improvement", solution_type="Automation",
            title="Business Process Automation",
            description="Automate manual, document-heavy, or multi-system workflows.",
            is_existing_offering=True, signals=("process",),
        ),
        SolutionCatalogEntry(
            id="custom-application-development", sector="general",
            pain_point="Cloud / Software Modernization", solution_type="Custom",
            title="Custom Application Development",
            description="Design and build applications tailored to the business.",
            is_existing_offering=True, signals=("technology",),
        ),
        SolutionCatalogEntry(
            id="azure-modernization", sector="general",
            pain_point="Cloud / Software Modernization", solution_type="Custom",
            title="Azure Modernization",
            description="Migrate and modernize legacy applications and infrastructure onto Azure.",
            is_existing_offering=True, signals=("technology",),
        ),
        SolutionCatalogEntry(
            id="architecture-review", sector="general",
            pain_point="Cloud / Software Modernization", solution_type="Custom",
            title="Architecture Review",
            description="Assess current architecture and produce a modernization roadmap.",
            is_existing_offering=True, signals=("technology",),
        ),
    )

    @classmethod
    def map_signals(
        cls,
        signals: dict[str, bool],
        catalog: list[SolutionCatalogEntry] | None = None,
    ) -> tuple[list[str], list[str]]:
        entries = catalog if catalog else cls._DEFAULT_CATALOG
        opportunities: list[str] = []
        services: list[str] = []
        for entry in entries:
            if not entry.is_existing_offering or not entry.signals:
                continue
            if not any(signals.get(signal) for signal in entry.signals):
                continue
            if entry.pain_point not in opportunities:
                opportunities.append(entry.pain_point)
            if entry.title not in services:
                services.append(entry.title)
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
