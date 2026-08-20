"""
Jurisdiction resolution -- maps a free-text Company.country string to the
platform's own ComplianceRuleset default.

Company.country is unvalidated free text (whatever was entered or
scraped) -- there's no ISO code, no canonical form anywhere upstream. This
is deliberately an explicit lookup table, not fuzzy matching: best-effort
against the country strings actually observed in this codebase's real
data, not an attempt at authoritative geo-classification. Extend the
alias sets as new country strings are observed, rather than guessing at
matching logic that could silently misclassify.

Unrecognized/missing geography resolves to "DEFAULT" -- the platform's
strictest known ruleset (opt-in), never a permissive guess.
"""

from __future__ import annotations

from app.domain.compliance.value_objects.compliance_ruleset import ComplianceRuleset

_US_ALIASES = frozenset(
    {
        "united states",
        "united states of america",
        "usa",
        "us",
        "u.s.",
        "u.s.a.",
    }
)

_EU_COUNTRIES = frozenset(
    {
        "austria",
        "belgium",
        "bulgaria",
        "croatia",
        "cyprus",
        "czechia",
        "czech republic",
        "denmark",
        "estonia",
        "finland",
        "france",
        "germany",
        "greece",
        "hungary",
        "ireland",
        "italy",
        "latvia",
        "lithuania",
        "luxembourg",
        "malta",
        "netherlands",
        "poland",
        "portugal",
        "romania",
        "slovakia",
        "slovenia",
        "spain",
        "sweden",
    }
)

DEFAULT_JURISDICTION_CODE = "DEFAULT"


class JurisdictionResolver:
    """Resolves a country string to a loaded ComplianceRuleset."""

    def __init__(self, rulesets: dict[str, ComplianceRuleset]) -> None:
        self._rulesets = rulesets

    def resolve(self, country: str | None) -> ComplianceRuleset:
        code = self._classify(country)
        ruleset = self._rulesets.get(code)
        if ruleset is not None:
            return ruleset
        return self._rulesets[DEFAULT_JURISDICTION_CODE]

    @staticmethod
    def _classify(country: str | None) -> str:
        if not country:
            return DEFAULT_JURISDICTION_CODE

        normalized = country.strip().lower()
        if normalized in _US_ALIASES:
            return "US"
        if normalized in _EU_COUNTRIES:
            return "EU"
        return DEFAULT_JURISDICTION_CODE
