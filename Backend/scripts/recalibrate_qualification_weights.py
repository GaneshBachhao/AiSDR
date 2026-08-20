"""
Outcome feedback loop recalibration pass (EPIC-12.2).

Offline, on-demand job -- there is no scheduler/cron infrastructure
anywhere in this codebase, so this runs by hand or via an external
scheduler invoking it, the same way `create_user.py` and
`seed_demo_data.py` are run directly rather than through the app.

Loads every Lead with captured `evidence_signals` (EPIC-12.2a) and every
recorded `OutcomeEvent` (EPIC-12.1), and reports -- per buying-signal
category -- whether Leads with that signal booked meetings at a different
rate than Leads without it. Deliberately stops at reporting the
correlation; it does not compute or write new
`QualificationScorer` weight overrides. Turning "hiring signal correlates
with 20% more meetings" into a specific weight delta is a human judgment
call, not a formula this script should make silently.

Honors the backlog's own framing of this story as a calendar gate, not a
one-shot computation: with too few (Lead, outcome) pairs, it reports
"insufficient data" rather than presenting noise as signal.

Usage (from Backend/, with the venv active -- run as a module, not a bare
script path, so the `app` package resolves on sys.path):

    python -m scripts.recalibrate_qualification_weights
    python -m scripts.recalibrate_qualification_weights --minimum-sample-size 50
"""

from __future__ import annotations

import argparse
import asyncio

from app.domain.outcome.enums.outcome_type import OutcomeType
from app.domain.outcome.services.signal_correlation_analyzer import (
    SignalCorrelationAnalyzer,
    SignalOutcomeRecord,
)
from app.infrastructure.configuration.database_settings import DatabaseSettings
from app.infrastructure.persistence.database.session import get_session_manager
from app.infrastructure.persistence.unit_of_work.sqlalchemy_unit_of_work import (
    SqlAlchemyUnitOfWork,
)

# Leads/outcomes are loaded in full rather than paged -- an offline
# analysis pass, not a user-facing listing, and real volumes are expected
# to be small for a long while yet (see the "insufficient data" path).
_MAX_LEADS = 10_000

_MEETING_REACHED_TYPES = frozenset({OutcomeType.MEETING_BOOKED, OutcomeType.WON})


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--minimum-sample-size",
        type=int,
        default=20,
        help="Minimum (Lead, outcome) pairs required before reporting correlations.",
    )
    return parser.parse_args()


async def main() -> None:
    args = _parse_args()

    settings = DatabaseSettings()
    manager = get_session_manager(settings)
    session = manager.create_session()

    try:
        uow = SqlAlchemyUnitOfWork(session=session)

        async with uow:
            leads = await uow.lead_repository.list(limit=_MAX_LEADS)
            outcomes = await uow.outcome_repository.list(limit=_MAX_LEADS)

        reached_meeting_lead_ids = {
            str(outcome.lead_id) for outcome in outcomes if outcome.outcome_type in _MEETING_REACHED_TYPES
        }

        records = [
            SignalOutcomeRecord(
                signals=lead.evidence_signals,
                reached_meeting=str(lead.id) in reached_meeting_lead_ids,
            )
            for lead in leads
            if lead.evidence_signals is not None
        ]

        report = SignalCorrelationAnalyzer.analyze(records, minimum_sample_size=args.minimum_sample_size)

        if report.insufficient_data:
            print(
                f"Insufficient data: {report.total_records} Lead(s) with captured evidence "
                f"signals, need at least {report.minimum_sample_size}. No correlations "
                "computed -- this is expected until the pipeline has been live long enough "
                "to accumulate real outcomes (see EPIC-12's backlog note)."
            )
            return

        print(f"Recalibration pass over {report.total_records} Lead(s) with captured evidence signals:\n")
        for correlation in report.correlations:
            print(
                f"  {correlation.signal:<12} present={correlation.meeting_rate_when_present:.0%}  "
                f"absent={correlation.meeting_rate_when_absent:.0%}  "
                f"diff={correlation.difference:+.0%}"
            )
        print(
            "\nThese are observed correlations only -- deciding whether/how much to adjust "
            "QualificationScorer weight_overrides for a Domain Profile is a human call."
        )
    finally:
        await session.close()


if __name__ == "__main__":
    asyncio.run(main())
