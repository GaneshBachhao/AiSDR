"""
OutcomeEvent persistence mapper.

OutcomeEvent is create-only (no update use case -- an event is either
recorded or deleted to correct a mistake), so there's no update_model()
here the way Lead/Recommendation/User have -- there's nothing that would
ever call it.
"""

from __future__ import annotations

from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.outcome.entities.outcome_event import OutcomeEvent
from app.domain.outcome.enums.outcome_type import OutcomeType
from app.domain.outcome.identifiers.outcome_event_id import OutcomeEventId
from app.infrastructure.persistence.models.outcome_event_model import OutcomeEventModel


class OutcomeEventMapper:
    """Maps OutcomeEvent domain entities and ORM models."""

    @staticmethod
    def to_domain(model: OutcomeEventModel) -> OutcomeEvent:
        event = OutcomeEvent(
            id=OutcomeEventId(model.id),
            lead_id=LeadId(model.lead_id),
            outcome_type=OutcomeType(model.outcome_type),
            notes=model.notes,
            occurred_at=model.occurred_at,
        )
        event.created_at = model.created_at
        event.updated_at = model.updated_at
        return event

    @staticmethod
    def to_model(entity: OutcomeEvent) -> OutcomeEventModel:
        return OutcomeEventModel(
            id=entity.id.value,
            lead_id=entity.lead_id.value,
            outcome_type=entity.outcome_type.value,
            notes=entity.notes,
            occurred_at=entity.occurred_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
