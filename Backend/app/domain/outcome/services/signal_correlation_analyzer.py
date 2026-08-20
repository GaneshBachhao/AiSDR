"""
SignalCorrelationAnalyzer -- the "recalibration pass" from EPIC-12.2.

A pure, stateless statistics service: no DB access, no AI call. It answers
"did leads with this evidence signal book more meetings than leads without
it?" over whatever (signals, outcome) pairs the caller already loaded.

Deliberately stops at reporting correlation, not auto-computing new
QualificationScorer weight overrides -- turning "hiring signal correlates
with 20% more meetings" into a specific weight delta is a human judgment
call, not a formula this service should invent. It also refuses to report
anything when the sample is too small, rather than presenting noise as
signal -- this mirrors the backlog's own framing of 12.2 as a calendar
gate, not a one-shot computation.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SignalOutcomeRecord:
    """One Lead's captured evidence signals and whether it booked a meeting."""

    signals: dict[str, bool]
    reached_meeting: bool


@dataclass(frozen=True, slots=True)
class SignalCorrelation:
    """Meeting-booked rate for one signal category, split by presence."""

    signal: str
    sample_size: int
    meeting_rate_when_present: float
    meeting_rate_when_absent: float

    @property
    def difference(self) -> float:
        return self.meeting_rate_when_present - self.meeting_rate_when_absent


@dataclass(frozen=True, slots=True)
class SignalCorrelationReport:
    """Result of a recalibration pass."""

    total_records: int
    minimum_sample_size: int
    insufficient_data: bool
    correlations: tuple[SignalCorrelation, ...] = ()


class SignalCorrelationAnalyzer:
    """Computes per-signal meeting-booked correlation over recorded outcomes."""

    @staticmethod
    def analyze(
        records: list[SignalOutcomeRecord],
        minimum_sample_size: int = 20,
    ) -> SignalCorrelationReport:
        total = len(records)
        if total < minimum_sample_size:
            return SignalCorrelationReport(
                total_records=total,
                minimum_sample_size=minimum_sample_size,
                insufficient_data=True,
            )

        signal_names: set[str] = set()
        for record in records:
            signal_names.update(record.signals.keys())

        correlations = tuple(
            sorted(
                (SignalCorrelationAnalyzer._correlate(records, signal) for signal in signal_names),
                key=lambda correlation: correlation.signal,
            )
        )

        return SignalCorrelationReport(
            total_records=total,
            minimum_sample_size=minimum_sample_size,
            insufficient_data=False,
            correlations=correlations,
        )

    @staticmethod
    def _correlate(records: list[SignalOutcomeRecord], signal: str) -> SignalCorrelation:
        with_signal = [record for record in records if record.signals.get(signal)]
        without_signal = [record for record in records if not record.signals.get(signal)]

        return SignalCorrelation(
            signal=signal,
            sample_size=len(records),
            meeting_rate_when_present=SignalCorrelationAnalyzer._meeting_rate(with_signal),
            meeting_rate_when_absent=SignalCorrelationAnalyzer._meeting_rate(without_signal),
        )

    @staticmethod
    def _meeting_rate(records: list[SignalOutcomeRecord]) -> float:
        if not records:
            return 0.0
        booked = sum(1 for record in records if record.reached_meeting)
        return booked / len(records)
