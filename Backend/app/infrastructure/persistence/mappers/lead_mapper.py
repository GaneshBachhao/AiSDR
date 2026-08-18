"""Lead domain <-> ORM mapper."""

from __future__ import annotations

from app.domain.company.identifiers.company_id import CompanyId
from app.domain.contact.identifiers.contact_id import ContactId
from app.domain.lead.entities.lead import Lead
from app.domain.lead.enums.lead_source import LeadSource
from app.domain.lead.enums.lead_status import LeadStatus
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.lead.value_objects.lead_score import LeadScore
from app.infrastructure.persistence.models.lead_model import LeadModel


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
        )

        lead.created_at = model.created_at
        lead.updated_at = model.updated_at

        return lead

    @staticmethod
    def to_model(entity: Lead) -> LeadModel:
        return LeadModel(
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
        )

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

        return model
