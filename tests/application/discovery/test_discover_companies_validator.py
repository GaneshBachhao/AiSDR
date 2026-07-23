"""
Unit Tests for DiscoverCompaniesValidator
"""

from app.application.discovery.validators.discover_companies_validator import (
    DiscoverCompaniesValidator,
)

from app.discovery.schemas.discovery_schema import (
    DiscoveryRequest,
)


def test_validator_accepts_valid_request():

    validator = DiscoverCompaniesValidator()

    request = DiscoveryRequest(

        industry="Healthcare",

        location="India",

        max_results=10,
    )

    result = validator.validate(request)

    assert result.success is True

    assert result.errors == []


def test_validator_requires_industry():

    validator = DiscoverCompaniesValidator()

    request = DiscoveryRequest(

        industry="",

        location="India",

        max_results=10,
    )

    result = validator.validate(request)

    assert result.success is False

    assert "Industry is required." in result.errors


def test_validator_requires_location():

    validator = DiscoverCompaniesValidator()

    request = DiscoveryRequest(

        industry="Healthcare",

        location="",

        max_results=10,
    )

    result = validator.validate(request)

    assert result.success is False

    assert "Location is required." in result.errors


def test_validator_rejects_invalid_max_results():

    validator = DiscoverCompaniesValidator()

    request = DiscoveryRequest(

        industry="Healthcare",

        location="India",

        max_results=0,
    )

    result = validator.validate(request)

    assert result.success is False