"""
Domain Profile loader.

Seed profiles for the 9 initial sectors (see docs/pamacore_aisdr_summary.md
§1) live in this directory as JSON, one file per sector, named after the
profile's ``name`` field with spaces replaced by underscores. Loading is a
pure infrastructure concern (file I/O) that produces the domain-layer
``DomainProfile`` value object -- domain services never touch the
filesystem directly.
"""

from __future__ import annotations

import json
from pathlib import Path

from app.domain.company_research.value_objects.domain_profile import DomainProfile

_PROFILES_DIR = Path(__file__).parent


def _profile_from_dict(data: dict) -> DomainProfile:
    return DomainProfile(
        name=data["name"],
        industry_keywords={key: tuple(values) for key, values in data.get("industry_keywords", {}).items()},
        negative_service_markers=tuple(data.get("negative_service_markers", ())),
        enterprise_exclusion_threshold=data.get("enterprise_exclusion_threshold", 500),
        enterprise_exclusion_markers=tuple(data.get("enterprise_exclusion_markers", ())),
        evidence_scope_keywords=tuple(data.get("evidence_scope_keywords", ())),
        scoring_weight_overrides=data.get("scoring_weight_overrides", {}),
    )


def load_domain_profile(sector: str) -> DomainProfile:
    """Load one named seed profile (e.g. "manufacturing", "financial services")."""

    file_name = sector.strip().lower().replace(" ", "_") + ".json"
    path = _PROFILES_DIR / file_name

    if not path.exists():
        raise ValueError(f"No domain profile found for sector '{sector}'.")

    data = json.loads(path.read_text(encoding="utf-8"))
    return _profile_from_dict(data)


def load_all_domain_profiles() -> dict[str, DomainProfile]:
    """Load every seed profile in this directory, keyed by profile name."""

    profiles: dict[str, DomainProfile] = {}

    for path in sorted(_PROFILES_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        profile = _profile_from_dict(data)
        profiles[profile.name] = profile

    return profiles


__all__ = [
    "load_all_domain_profiles",
    "load_domain_profile",
]
