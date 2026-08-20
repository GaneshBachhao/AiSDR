from __future__ import annotations

from app.domain.outcome.services.signal_correlation_analyzer import (
    SignalCorrelationAnalyzer,
    SignalOutcomeRecord,
)


def _record(hiring: bool, reached_meeting: bool) -> SignalOutcomeRecord:
    return SignalOutcomeRecord(signals={"hiring": hiring, "growth": False}, reached_meeting=reached_meeting)


def test_reports_insufficient_data_below_the_minimum_sample_size() -> None:
    records = [_record(True, True), _record(False, False)]

    report = SignalCorrelationAnalyzer.analyze(records, minimum_sample_size=5)

    assert report.insufficient_data is True
    assert report.total_records == 2
    assert report.correlations == ()


def test_reports_a_clear_correlation_when_a_signal_predicts_meetings() -> None:
    records = [_record(True, True) for _ in range(10)] + [_record(False, False) for _ in range(10)]

    report = SignalCorrelationAnalyzer.analyze(records, minimum_sample_size=5)

    assert report.insufficient_data is False
    hiring = next(c for c in report.correlations if c.signal == "hiring")
    assert hiring.meeting_rate_when_present == 1.0
    assert hiring.meeting_rate_when_absent == 0.0
    assert hiring.difference == 1.0


def test_reports_no_difference_when_a_signal_does_not_predict_meetings() -> None:
    records = [_record(True, True), _record(True, False)] * 5

    report = SignalCorrelationAnalyzer.analyze(records, minimum_sample_size=5)

    hiring = next(c for c in report.correlations if c.signal == "hiring")
    assert hiring.meeting_rate_when_present == 0.5
    assert hiring.difference == 0.5


def test_covers_every_signal_key_seen_across_records() -> None:
    records = [
        SignalOutcomeRecord(signals={"hiring": True}, reached_meeting=True),
        SignalOutcomeRecord(signals={"growth": True}, reached_meeting=False),
    ] * 3

    report = SignalCorrelationAnalyzer.analyze(records, minimum_sample_size=5)

    signals_covered = {c.signal for c in report.correlations}
    assert signals_covered == {"hiring", "growth"}
