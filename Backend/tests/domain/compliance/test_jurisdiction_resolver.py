from __future__ import annotations

from app.domain.compliance.services.jurisdiction_resolver import JurisdictionResolver
from app.domain.compliance.value_objects.compliance_ruleset import ComplianceRuleset


def _rulesets() -> dict[str, ComplianceRuleset]:
    return {
        "US": ComplianceRuleset(
            jurisdiction_code="US",
            regime_name="CAN-SPAM",
            consent_model="opt-out",
            requires_physical_address=True,
        ),
        "EU": ComplianceRuleset(
            jurisdiction_code="EU",
            regime_name="GDPR",
            consent_model="opt-in",
        ),
        "DEFAULT": ComplianceRuleset(
            jurisdiction_code="DEFAULT",
            regime_name="Unclassified",
            consent_model="opt-in",
        ),
    }


def test_resolves_common_us_aliases() -> None:
    resolver = JurisdictionResolver(_rulesets())

    for alias in ("United States", "USA", "us", "U.S.", "  United States of America  "):
        assert resolver.resolve(alias).jurisdiction_code == "US"


def test_resolves_eu_member_states() -> None:
    resolver = JurisdictionResolver(_rulesets())

    for country in ("Germany", "france", "Netherlands"):
        assert resolver.resolve(country).jurisdiction_code == "EU"


def test_unrecognized_country_falls_back_to_default() -> None:
    resolver = JurisdictionResolver(_rulesets())

    result = resolver.resolve("Narnia")

    assert result.jurisdiction_code == "DEFAULT"


def test_none_country_falls_back_to_default() -> None:
    resolver = JurisdictionResolver(_rulesets())

    result = resolver.resolve(None)

    assert result.jurisdiction_code == "DEFAULT"


def test_default_is_the_strictest_regime_not_a_permissive_guess() -> None:
    resolver = JurisdictionResolver(_rulesets())

    result = resolver.resolve(None)

    assert result.consent_model == "opt-in"


def test_missing_default_key_raises_key_error_rather_than_silently_picking_one() -> None:
    resolver = JurisdictionResolver({"US": _rulesets()["US"]})

    try:
        resolver.resolve("Narnia")
        raised = False
    except KeyError:
        raised = True

    assert raised
