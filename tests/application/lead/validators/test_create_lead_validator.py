from app.application.lead.commands.create_lead import CreateLeadCommand
from app.application.lead.validators.create_lead_validator import (
    CreateLeadValidator,
)


def create_command(**kwargs) -> CreateLeadCommand:
    data = {
        "company_name": "Acme Ltd",
        "contact_name": "John Doe",
        "email": "john@acme.com",
        "phone": "9876543210",
        "website": "https://acme.com",
    }
    data.update(kwargs)
    return CreateLeadCommand(**data)


def test_validator_accepts_valid_command():
    validator = CreateLeadValidator()

    result = validator.validate(create_command())

    assert result.is_valid


def test_validator_requires_company_name():
    validator = CreateLeadValidator()

    result = validator.validate(
        create_command(company_name="")
    )

    assert not result.is_valid
    assert result.has_error("company_name")


def test_validator_requires_contact_name():
    validator = CreateLeadValidator()

    result = validator.validate(
        create_command(contact_name="")
    )

    assert not result.is_valid
    assert result.has_error("contact_name")


def test_validator_rejects_invalid_email():
    validator = CreateLeadValidator()

    result = validator.validate(
        create_command(email="invalid")
    )

    assert not result.is_valid
    assert result.has_error("email")


def test_validator_rejects_invalid_website():
    validator = CreateLeadValidator()

    result = validator.validate(
        create_command(website="google.com")
    )

    assert not result.is_valid
    assert result.has_error("website")


def test_validator_rejects_short_phone():
    validator = CreateLeadValidator()

    result = validator.validate(
        create_command(phone="123")
    )

    assert not result.is_valid
    assert result.has_error("phone")