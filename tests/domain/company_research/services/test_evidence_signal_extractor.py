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


def test_scale_signal_strong_marker():
    assert EvidenceSignalExtractor.scale_signal("the company reported $50 million in revenue") == "strong"


def test_scale_signal_moderate_marker():
    assert EvidenceSignalExtractor.scale_signal("an established global company") == "moderate"


def test_scale_signal_none():
    assert EvidenceSignalExtractor.scale_signal("a small local shop") == "none"


def test_classify_evidence_confirmed_need():
    signals = {"hiring": True, "technology": True}
    assert EvidenceSignalExtractor.classify_evidence(signals, evidence_count=3) == "Confirmed Need"


def test_classify_evidence_strong_opportunity_signal():
    signals = {"hiring": True}
    assert EvidenceSignalExtractor.classify_evidence(signals, evidence_count=1) == "Strong Opportunity Signal"


def test_classify_evidence_reasonable_business_hypothesis():
    signals = {"hiring": False}
    assert EvidenceSignalExtractor.classify_evidence(signals, evidence_count=1) == "Reasonable Business Hypothesis"


def test_classify_evidence_unverified_assumption_when_nothing_found():
    signals = {"hiring": False}
    assert EvidenceSignalExtractor.classify_evidence(signals, evidence_count=0) == "Unverified Assumption"
