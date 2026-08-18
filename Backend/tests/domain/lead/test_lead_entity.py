from __future__ import annotations

from app.domain.company.identifiers.company_id import CompanyId
from app.domain.contact.identifiers.contact_id import ContactId
from app.domain.lead.entities.lead import Lead
from app.domain.lead.enums.lead_source import LeadSource
from app.domain.lead.enums.lead_status import LeadStatus
from app.domain.lead.value_objects.lead_score import LeadScore


def _lead(**overrides) -> Lead:
    defaults = dict(company_id=CompanyId(), contact_id=ContactId())
    defaults.update(overrides)
    return Lead(**defaults)


def test_lead_defaults_to_new_and_not_qualified() -> None:
    lead = _lead()

    assert lead.status is LeadStatus.NEW
    assert lead.is_qualified is False
    assert lead.source is LeadSource.OTHER


def test_lead_strips_notes_and_blank_notes_become_none() -> None:
    lead = _lead(notes="  some notes  ")
    assert lead.notes == "some notes"

    blank = _lead(notes="   ")
    assert blank.notes is None


def test_update_status_to_qualified_cascades_is_qualified() -> None:
    # Regression guard for a real, live-verified behavior (EPIC-F05):
    # setting status to QUALIFIED must flip is_qualified too, not leave
    # the frontend to compute it separately.
    lead = _lead()

    lead.update_status(LeadStatus.QUALIFIED)

    assert lead.status is LeadStatus.QUALIFIED
    assert lead.is_qualified is True


def test_update_status_to_a_non_qualified_status_clears_is_qualified() -> None:
    lead = _lead()
    lead.update_status(LeadStatus.QUALIFIED)

    lead.update_status(LeadStatus.CONTACTED)

    assert lead.is_qualified is False


def test_qualify_disqualify_convert_close() -> None:
    lead = _lead()

    lead.qualify()
    assert lead.status is LeadStatus.QUALIFIED
    assert lead.is_qualified is True

    lead.disqualify()
    assert lead.status is LeadStatus.DISQUALIFIED
    assert lead.is_qualified is False

    lead.convert()
    assert lead.status is LeadStatus.CONVERTED
    assert lead.is_qualified is False

    lead.close()
    assert lead.status is LeadStatus.CLOSED


def test_update_contact_source_score() -> None:
    lead = _lead()
    new_contact = ContactId()

    lead.update_contact(new_contact)
    lead.update_source(LeadSource.AI_RESEARCH)
    lead.update_score(LeadScore(75))

    assert lead.contact_id == new_contact
    assert lead.source is LeadSource.AI_RESEARCH
    assert lead.score.value == 75


def test_update_notes_strips_and_blank_clears() -> None:
    lead = _lead()

    lead.update_notes("  hello  ")
    assert lead.notes == "hello"

    lead.update_notes("   ")
    assert lead.notes is None


def test_lead_id_defaults_to_a_generated_identifier() -> None:
    lead = _lead()

    assert lead.id is not None
