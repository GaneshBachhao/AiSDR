"""
Domain Profile — per-sector configuration for company_research.

Replaces hardcoded keyword tables scattered across domain services with a
single injectable data object, so adding or tuning a domain (Healthcare,
Pharma, Logistics, ...) is a config change, not a change to the shared
core engine. See docs/pamacore_aisdr_summary.md §5 for the full rationale.

This is a pure data container -- no I/O, no defaults baked in beyond what
makes an empty profile safely inert (empty keyword sets simply never
match anything). Loading named profiles from disk is an infrastructure
concern (see app.infrastructure.configuration.domain_profiles).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DomainProfile:
    """Per-sector vocabulary and rules consumed by domain_research services."""

    name: str

    industry_keywords: dict[str, tuple[str, ...]] = field(default_factory=dict)
    negative_service_markers: tuple[str, ...] = ()

    enterprise_exclusion_threshold: int = 500
    enterprise_exclusion_markers: tuple[str, ...] = ()

    evidence_scope_keywords: tuple[str, ...] = ()
    scoring_weight_overrides: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Domain profile name is required.")

        if self.enterprise_exclusion_threshold <= 0:
            raise ValueError("enterprise_exclusion_threshold must be positive.")
