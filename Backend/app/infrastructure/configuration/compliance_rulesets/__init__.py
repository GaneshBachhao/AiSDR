"""
Compliance Ruleset loader.

Rulesets live in this directory as JSON, one file per jurisdiction,
named after the ruleset's own ``jurisdiction_code`` field (lowercased).
Loading is a pure infrastructure concern (file I/O) that produces the
domain-layer ``ComplianceRuleset`` value object -- domain services never
touch the filesystem directly.
"""

from __future__ import annotations

import json
from pathlib import Path

from app.domain.compliance.value_objects.compliance_ruleset import ComplianceRuleset

_RULESETS_DIR = Path(__file__).parent


def _ruleset_from_dict(data: dict) -> ComplianceRuleset:
    return ComplianceRuleset(
        jurisdiction_code=data["jurisdiction_code"],
        regime_name=data["regime_name"],
        consent_model=data.get("consent_model", "opt-in"),
        requires_unsubscribe_link=data.get("requires_unsubscribe_link", True),
        requires_physical_address=data.get("requires_physical_address", False),
        cooldown_days=data.get("cooldown_days"),
        notes=data.get("notes", ""),
    )


def load_compliance_ruleset(jurisdiction_code: str) -> ComplianceRuleset:
    """Load one named ruleset (e.g. "us", "eu", "default")."""

    file_name = jurisdiction_code.strip().lower() + ".json"
    path = _RULESETS_DIR / file_name

    if not path.exists():
        raise ValueError(f"No compliance ruleset found for jurisdiction '{jurisdiction_code}'.")

    data = json.loads(path.read_text(encoding="utf-8"))
    return _ruleset_from_dict(data)


def load_all_compliance_rulesets() -> dict[str, ComplianceRuleset]:
    """Load every ruleset in this directory, keyed by jurisdiction_code."""

    rulesets: dict[str, ComplianceRuleset] = {}

    for path in sorted(_RULESETS_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        ruleset = _ruleset_from_dict(data)
        rulesets[ruleset.jurisdiction_code] = ruleset

    return rulesets


__all__ = [
    "load_all_compliance_rulesets",
    "load_compliance_ruleset",
]
