from app.domain.company_research.services.opportunity_mapper import OpportunityMapper


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
