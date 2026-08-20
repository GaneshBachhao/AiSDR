"""Compliance response DTOs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ComplianceRulesetResponseDTO:
    """Standard ComplianceRuleset response DTO."""

    jurisdiction_code: str
    regime_name: str
    consent_model: str
    requires_unsubscribe_link: bool
    requires_physical_address: bool
    cooldown_days: int | None
    notes: str


@dataclass(slots=True)
class LeadComplianceRulesetResponseDTO:
    """The resolved ruleset for one Lead, plus what it was resolved from."""

    lead_id: str
    company_country: str | None
    ruleset: ComplianceRulesetResponseDTO
