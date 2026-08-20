"""
Compliance Ruleset — per-jurisdiction consent rules for outbound contact.

Mirrors app.domain.company_research.value_objects.domain_profile.DomainProfile's
shape and rationale: a small, named, data-driven rule profile instead of
hardcoded logic, so tuning a jurisdiction's rules is a config change, not
a code change. This is a pure data container -- no I/O; loading named
rulesets from disk is an infrastructure concern (see
app.infrastructure.configuration.compliance_rulesets).

These rulesets are the platform's own conservative guardrail defaults,
not authoritative legal advice -- CAN-SPAM/GDPR/TCPA classification here
is a best-effort default, not a legal determination.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class ComplianceRuleset:
    """Per-jurisdiction consent/deliverability rules."""

    jurisdiction_code: str
    regime_name: str

    consent_model: Literal["opt-out", "opt-in"] = "opt-in"
    requires_unsubscribe_link: bool = True
    requires_physical_address: bool = False
    cooldown_days: int | None = None

    notes: str = ""

    def __post_init__(self) -> None:
        if not self.jurisdiction_code or not self.jurisdiction_code.strip():
            raise ValueError("Compliance ruleset jurisdiction_code is required.")

        if self.cooldown_days is not None and self.cooldown_days < 0:
            raise ValueError("cooldown_days cannot be negative.")
