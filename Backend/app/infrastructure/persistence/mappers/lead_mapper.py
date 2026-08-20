"""Lead domain <-> ORM mapper."""

from __future__ import annotations

from app.domain.company.identifiers.company_id import CompanyId
from app.domain.contact.identifiers.contact_id import ContactId
from app.domain.lead.entities.lead import Lead
from app.domain.lead.enums.lead_review_status import LeadReviewStatus
from app.domain.lead.enums.lead_source import LeadSource
from app.domain.lead.enums.lead_status import LeadStatus
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.lead.value_objects.lead_score import LeadScore
from app.infrastructure.persistence.models.lead_model import LeadModel

# Fixed, closed set of buying-signal categories (EPIC-12) -- matches
# EvidenceSignalExtractor.SIGNAL_KEYWORDS in app/domain/company_research.
# Duplicated here rather than imported: the persistence layer shouldn't
# depend on company_research's domain module for a fixed literal list, the
# same way the rest of this mapper doesn't import company_research types.
_SIGNAL_KEYS = ("hiring", "growth", "technology", "ai", "process", "funding")


class LeadMapper:
    """Map Lead aggregates to/from persistence models."""

    @staticmethod
    def to_domain(model: LeadModel) -> Lead:
        lead = Lead(
            id=LeadId(model.id),
            company_id=CompanyId(model.company_id),
            contact_id=ContactId(model.contact_id),
            source=LeadSource(model.source),
            status=LeadStatus(model.status),
            score=(model.score if isinstance(model.score, LeadScore) else LeadScore(model.score)),
            notes=model.notes,
            is_qualified=model.is_qualified,
            review_status=LeadReviewStatus(model.review_status),
            review_submitted_at=model.review_submitted_at,
            review_decided_at=model.review_decided_at,
            review_notes=model.review_notes,
            evidence_signals=LeadMapper._unflatten_signals(model),
        )

        lead.created_at = model.created_at
        lead.updated_at = model.updated_at

        return lead

    @staticmethod
    def to_model(entity: Lead) -> LeadModel:
        model = LeadModel(
            id=entity.id.value,
            company_id=entity.company_id.value,
            contact_id=entity.contact_id.value,
            source=entity.source.value,
            status=entity.status.value,
            # Preserve the domain Value Object.
            # LeadScoreType handles LeadScore -> INTEGER.
            score=entity.score,
            notes=entity.notes,
            is_qualified=entity.is_qualified,
            review_status=entity.review_status.value,
            review_submitted_at=entity.review_submitted_at,
            review_decided_at=entity.review_decided_at,
            review_notes=entity.review_notes,
        )
        LeadMapper._flatten_signals(model, entity)
        return model

    @staticmethod
    def update_model(
        model: LeadModel,
        entity: Lead,
    ) -> LeadModel:
        model.company_id = entity.company_id.value
        model.contact_id = entity.contact_id.value
        model.source = entity.source.value
        model.status = entity.status.value

        # Preserve the domain Value Object.
        # LeadScoreType handles LeadScore -> INTEGER.
        model.score = entity.score

        model.notes = entity.notes
        model.is_qualified = entity.is_qualified
        model.review_status = entity.review_status.value
        model.review_submitted_at = entity.review_submitted_at
        model.review_decided_at = entity.review_decided_at
        model.review_notes = entity.review_notes
        LeadMapper._flatten_signals(model, entity)

        return model

    @staticmethod
    def _flatten_signals(model: LeadModel, entity: Lead) -> None:
        signals = entity.evidence_signals
        for key in _SIGNAL_KEYS:
            setattr(model, f"signal_{key}", None if signals is None else signals.get(key, False))

    @staticmethod
    def _unflatten_signals(model: LeadModel) -> dict[str, bool] | None:
        values = {key: getattr(model, f"signal_{key}") for key in _SIGNAL_KEYS}
        if all(value is None for value in values.values()):
            return None
        return {key: bool(value) for key, value in values.items()}
