from __future__ import annotations

import pytest

from app.domain.assessment.identifiers.assessment_id import AssessmentId
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.qualification.entities.qualification import Qualification
from app.infrastructure.persistence.repositories.qualification.sqlalchemy_qualification_repository import (
    SQLAlchemyQualificationRepository,
)


class DummyResult:
    def __init__(self, value):
        self._value = value

    def scalar_one_or_none(self):
        return self._value


class DummySession:
    def __init__(self):
        self.added_models = []

    async def execute(self, statement):
        return DummyResult(None)

    def add(self, model):
        self.added_models.append(model)


@pytest.mark.asyncio
async def test_qualification_repository_add_and_exists():
    session = DummySession()
    repository = SQLAlchemyQualificationRepository(session=session)

    qualification = Qualification(
        lead_id=LeadId("00000000-0000-0000-0000-000000000001"),
        assessment_id=AssessmentId("00000000-0000-0000-0000-000000000002"),
    )

    await repository.add(qualification)

    assert len(session.added_models) == 1
    assert session.added_models[0].id == qualification.id.value

    exists = await repository.exists(qualification.id)
    assert exists is False
