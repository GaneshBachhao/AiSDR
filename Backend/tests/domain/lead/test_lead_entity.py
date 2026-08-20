from __future__ import annotations

import pytest

from app.domain.company.identifiers.company_id import CompanyId
from app.domain.contact.identifiers.contact_id import ContactId
from app.domain.lead.entities.lead import Lead
from app.domain.lead.enums.lead_review_status import LeadReviewStatus
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


def test_lead_review_gate_defaults_to_not_submitted() -> None:
    lead = _lead()

    assert lead.review_status is LeadReviewStatus.NOT_SUBMITTED
    assert lead.review_submitted_at is None
    assert lead.review_decided_at is None
    assert lead.review_notes is None


def test_evidence_signals_defaults_to_none() -> None:
    lead = _lead()

    assert lead.evidence_signals is None


def test_evidence_signals_accepts_a_captured_dict() -> None:
    lead = _lead(evidence_signals={"hiring": True, "growth": False})

    assert lead.evidence_signals == {"hiring": True, "growth": False}


def test_submit_for_review_moves_to_pending_and_stamps_submitted_at() -> None:
    lead = _lead()

    lead.submit_for_review()

    assert lead.review_status is LeadReviewStatus.PENDING_REVIEW
    assert lead.review_submitted_at is not None


def test_submit_for_review_twice_raises() -> None:
    lead = _lead()
    lead.submit_for_review()

    with pytest.raises(ValueError, match="already pending review or approved"):
        lead.submit_for_review()


def test_approve_requires_pending_review() -> None:
    lead = _lead()

    with pytest.raises(ValueError, match="must be pending review before approval"):
        lead.approve()


def test_approve_moves_to_approved_and_stamps_decided_at() -> None:
    lead = _lead()
    lead.submit_for_review()

    lead.approve(notes="Looks solid, approved.")

    assert lead.review_status is LeadReviewStatus.APPROVED
    assert lead.review_decided_at is not None
    assert lead.review_notes == "Looks solid, approved."


def test_approve_twice_raises() -> None:
    lead = _lead()
    lead.submit_for_review()
    lead.approve()

    with pytest.raises(ValueError, match="must be pending review before approval"):
        lead.approve()


def test_submit_for_review_after_approved_raises() -> None:
    """An approved Lead cannot be silently reset to pending -- the whole
    point of the gate is that approval is a deliberate, terminal-for-now
    decision, not something a stray resubmission can undo."""
    lead = _lead()
    lead.submit_for_review()
    lead.approve()

    with pytest.raises(ValueError, match="already pending review or approved"):
        lead.submit_for_review()


def test_reject_requires_pending_review() -> None:
    lead = _lead()

    with pytest.raises(ValueError, match="must be pending review before rejection"):
        lead.reject()


def test_reject_moves_to_rejected_and_stamps_decided_at() -> None:
    lead = _lead()
    lead.submit_for_review()

    lead.reject(notes="Missing a verified contact email.")

    assert lead.review_status is LeadReviewStatus.REJECTED
    assert lead.review_decided_at is not None
    assert lead.review_notes == "Missing a verified contact email."


def test_rejected_lead_can_be_resubmitted() -> None:
    """A rejected Lead isn't a dead end -- a rep can fix the issue and
    resubmit, matching how this gate would actually be used."""
    lead = _lead()
    lead.submit_for_review()
    lead.reject()

    lead.submit_for_review()

    assert lead.review_status is LeadReviewStatus.PENDING_REVIEW


def test_reject_after_approved_raises() -> None:
    lead = _lead()
    lead.submit_for_review()
    lead.approve()

    with pytest.raises(ValueError, match="must be pending review before rejection"):
        lead.reject()


def test_approve_without_notes_leaves_review_notes_unset() -> None:
    lead = _lead()
    lead.submit_for_review()

    lead.approve()

    assert lead.review_notes is None
