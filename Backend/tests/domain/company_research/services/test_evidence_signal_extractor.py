from app.domain.company_research.services.evidence_signal_extractor import (
    EvidenceSignalExtractor,
)


def test_extract_signals_detects_hiring_and_technology():
    signals = EvidenceSignalExtractor.extract_signals("the company is hiring for cloud and software roles")
    assert signals["hiring"] is True
    assert signals["technology"] is True
    assert signals["funding"] is False


def test_trigger_event_combines_active_signals():
    event = EvidenceSignalExtractor.trigger_event({"hiring": True, "growth": True, "funding": False})
    assert event == "technology hiring, growth / expansion"


def test_trigger_event_none_when_no_signals():
    assert EvidenceSignalExtractor.trigger_event({"hiring": False, "growth": False, "funding": False}) is None


def test_classify_evidence_confirmed_need_requires_company_specific_evidence():
    signals = {"hiring": True, "technology": True}
    company_specific_signals = {"hiring": True, "technology": True}
    assert (
        EvidenceSignalExtractor.classify_evidence(
            signals,
            evidence_count=3,
            company_specific_signals=company_specific_signals,
            company_specific_evidence_count=2,
        )
        == "Confirmed Need"
    )


def test_classify_evidence_all_industry_evidence_can_never_reach_confirmed_need():
    """Regression guard: industry-general noise must never fake company-level
    confidence, even when the combined-text signal count would otherwise
    qualify for Confirmed Need."""
    signals = {"hiring": True, "technology": True}
    # No company_specific_signals/company_specific_evidence_count passed --
    # exactly what happens when all evidence is industry_general.
    assert EvidenceSignalExtractor.classify_evidence(signals, evidence_count=3) == "Strong Opportunity Signal"


def test_classify_evidence_confirmed_need_requires_at_least_two_company_specific_items():
    signals = {"hiring": True, "technology": True}
    company_specific_signals = {"hiring": True, "technology": True}
    # Only one company-specific evidence item -- still capped below Confirmed Need.
    assert (
        EvidenceSignalExtractor.classify_evidence(
            signals,
            evidence_count=3,
            company_specific_signals=company_specific_signals,
            company_specific_evidence_count=1,
        )
        == "Strong Opportunity Signal"
    )


def test_classify_evidence_strong_opportunity_signal():
    signals = {"hiring": True}
    assert EvidenceSignalExtractor.classify_evidence(signals, evidence_count=1) == "Strong Opportunity Signal"


def test_classify_evidence_reasonable_business_hypothesis():
    signals = {"hiring": False}
    assert (
        EvidenceSignalExtractor.classify_evidence(signals, evidence_count=1)
        == "Reasonable Business Hypothesis"
    )


def test_classify_evidence_unverified_assumption_when_nothing_found():
    signals = {"hiring": False}
    assert EvidenceSignalExtractor.classify_evidence(signals, evidence_count=0) == "Unverified Assumption"


def test_classify_scope_exact_name_match_is_company_specific():
    text = "acme manufacturing is hiring cloud engineers"
    assert EvidenceSignalExtractor.classify_scope(text, "Acme Manufacturing") == "company_specific"


def test_classify_scope_first_word_match_tolerates_legal_suffix_variation():
    text = "acme manufacturing pvt ltd announced a new facility"
    assert EvidenceSignalExtractor.classify_scope(text, "Acme Manufacturing") == "company_specific"


def test_classify_scope_no_name_mention_is_industry_general():
    text = "the manufacturing sector overall is investing in automation"
    assert EvidenceSignalExtractor.classify_scope(text, "Acme Manufacturing") == "industry_general"


def test_classify_scope_empty_company_name_is_industry_general():
    assert EvidenceSignalExtractor.classify_scope("some text", "") == "industry_general"
