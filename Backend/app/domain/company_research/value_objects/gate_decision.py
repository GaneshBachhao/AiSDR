from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class GateDecision:
    """Outcome of the deterministic pre-verification gate for a single candidate.

    ``reason`` is a stable machine-readable code (e.g. ``"blocked_domain"``),
    not a display string, so callers can branch on it or aggregate rejection
    metrics without string parsing.
    """

    accepted: bool
    reason: str
