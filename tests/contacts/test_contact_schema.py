"""
Tests for Contact Schemas.
"""

import pytest
from pydantic import ValidationError

from app.contacts.enums.contact_source import (
    ContactSource,
)

from app.contacts.enums.contact_status import (
    ContactStatus,
)

from app.contacts.schemas.contact_schema import (
    ContactCreate,
)


def test_create_contact():

    contact = ContactCreate(

        lead_id=1,

        full_name="John Doe",

        email="john@example.com",
    )

    assert contact.lead_id == 1

    assert contact.full_name == "John Doe"

    assert contact.status == ContactStatus.ACTIVE

    assert contact.source == ContactSource.MANUAL

    assert contact.is_primary is False


def test_invalid_email():

    with pytest.raises(
        ValidationError,
    ):

        ContactCreate(

            lead_id=1,

            full_name="John Doe",

            email="invalid-email",
        )


def test_confidence_score_validation():

    with pytest.raises(
        ValidationError,
    ):

        ContactCreate(

            lead_id=1,

            full_name="John Doe",

            email="john@example.com",

            confidence_score=1.5,
        )


def test_optional_fields():

    contact = ContactCreate(

        lead_id=1,

        full_name="Jane Doe",

        email="jane@example.com",

        job_title="CEO",
    )

    assert contact.job_title == "CEO"