from app.domain.company_research.services.opportunity_mapper import OpportunityMapper
from app.domain.recommendation.value_objects.solution_catalog_entry import (
    SolutionCatalogEntry,
)


def test_map_signals_ai_signal_maps_to_ai_consulting():
    opportunities, services = OpportunityMapper.map_signals({"ai": True})
    assert "AI / Generative AI" in opportunities
    assert "AI Consulting" in services


def test_map_signals_falls_back_to_generic_modernization():
    opportunities, services = OpportunityMapper.map_signals({})
    assert opportunities == ["Technology modernization"]
    assert "Architecture Review" in services


def test_map_signals_deduplicates_services():
    _, services = OpportunityMapper.map_signals({"technology": True})
    assert len(services) == len(set(services))


def test_service_matches_requested_direct_substring():
    assert OpportunityMapper.service_matches_requested(
        "Azure Modernization", ["azure modernization"]
    )


def test_service_matches_requested_via_alias():
    assert OpportunityMapper.service_matches_requested(
        "Business Process Automation", ["workflow automation"]
    )


def test_service_matches_requested_false_for_unrelated():
    assert not OpportunityMapper.service_matches_requested("AI Consulting", ["cloud migration"])


def test_any_service_matches_false_when_nothing_requested():
    assert OpportunityMapper.any_service_matches(["AI Consulting"], []) is False


def test_map_signals_with_injected_catalog_matches_the_default_fallback():
    """Regression guard: the real catalog (general.json, loaded via
    infrastructure) must produce identical results to the domain-owned
    default -- proving there's genuinely one source of truth, not two."""
    default_opportunities, default_services = OpportunityMapper.map_signals({"ai": True})
    catalog = [
        SolutionCatalogEntry(
            id="ai-consulting", sector="general", pain_point="AI / Generative AI",
            solution_type="AI Agent", title="AI Consulting", description="x",
            is_existing_offering=True, signals=("ai",),
        )
    ]
    catalog_opportunities, catalog_services = OpportunityMapper.map_signals(
        {"ai": True}, catalog
    )
    assert catalog_opportunities == default_opportunities
    assert catalog_services == default_services


def test_map_signals_ignores_non_existing_offering_catalog_entries():
    catalog = [
        SolutionCatalogEntry(
            id="generic-idea", sector="retail", pain_point="Something",
            solution_type="Chatbot", title="Generic Retail Bot", description="x",
            is_existing_offering=False, signals=("ai",),
        )
    ]
    opportunities, services = OpportunityMapper.map_signals({"ai": True}, catalog)
    # No existing-offering entry matched -- falls back to the generic default.
    assert opportunities == ["Technology modernization"]
    assert "Generic Retail Bot" not in services


def test_map_signals_ignores_catalog_entries_with_no_signals():
    catalog = [
        SolutionCatalogEntry(
            id="no-signals", sector="general", pain_point="Something",
            solution_type="Custom", title="Untriggerable", description="x",
            is_existing_offering=True, signals=(),
        )
    ]
    opportunities, _ = OpportunityMapper.map_signals({"ai": True}, catalog)
    assert opportunities == ["Technology modernization"]
