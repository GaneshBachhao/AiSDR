"""
AI Solution Catalog entry -- a first-class, shared reference list of
sector/pain-point-mapped solutions, consumed by both the AI-driven
``generate`` recommendation flow and company_research's deterministic
``OpportunityMapper``. See docs/pamacore_aisdr_summary.md §7/§10.

Two kinds of entries:
- ``is_existing_offering=True``, ``sector="general"`` -- the handful of
  real, sector-agnostic Pamacore service lines (Custom Application
  Development, Azure Modernization, ...). These carry ``signals`` so
  ``OpportunityMapper`` can match them deterministically the same way it
  already does today.
- ``is_existing_offering=False``, a specific ``sector`` -- generic,
  sector-appropriate opportunity ideas (seeded from the architecture doc's
  Appendix A) that the AI can propose when no existing offering fits, but
  which must always be labeled as generic, never blurred with a real
  offering.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.recommendation.enums.solution_type import SolutionType


@dataclass(frozen=True)
class SolutionCatalogEntry:
    id: str
    sector: str
    pain_point: str
    solution_type: SolutionType
    title: str
    description: str
    is_existing_offering: bool
    signals: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if isinstance(self.solution_type, str):
            object.__setattr__(self, "solution_type", SolutionType(self.solution_type))
