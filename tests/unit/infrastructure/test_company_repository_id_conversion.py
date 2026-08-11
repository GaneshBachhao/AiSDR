from uuid import uuid4
from unittest.mock import AsyncMock, Mock

import pytest

from app.domain.company.identifiers.company_id import CompanyId
from app.infrastructure.persistence.repositories.base.sqlalchemy_repository import (
    SqlAlchemyRepository,
)
from app.infrastructure.persistence.models.company_model import CompanyModel


class DummyRepository(SqlAlchemyRepository):
    model_type = CompanyModel


@pytest.mark.asyncio
async def test_repository_unwraps_identifier_before_query() -> None:
    session = AsyncMock()
    session.execute.return_value.scalar_one_or_none.return_value = None

    repository = DummyRepository(session=session, mapper=Mock())
    company_id = CompanyId(uuid4())

    await repository.get_by_id(company_id)

    statement = session.execute.call_args.args[0]
    # SQLAlchemy binds the UUID value, not the CompanyId object.
    assert company_id.value in statement.compile().params.values()
