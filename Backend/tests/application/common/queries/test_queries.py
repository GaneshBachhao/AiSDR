# tests/application/common/queries/test_queries.py

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.application.common.queries import (
    Query,
    QueryHandler,
)


class GetTestQuery(Query):
    """
    Test query.
    """

    identifier: int


class TestQueryHandler(
    QueryHandler[
        GetTestQuery,
        str,
    ],
):
    """
    Test query handler.
    """

    async def handle(
        self,
        query: GetTestQuery,
    ) -> str:
        return str(query.identifier)


def test_query_accepts_valid_data() -> None:
    query = GetTestQuery(
        identifier=100,
    )

    assert query.identifier == 100


def test_query_is_immutable() -> None:
    query = GetTestQuery(
        identifier=100,
    )

    with pytest.raises(ValidationError):
        query.identifier = 200


def test_query_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        GetTestQuery(
            identifier=100,
            unknown="value",
        )


@pytest.mark.asyncio
async def test_query_handler_executes() -> None:
    handler = TestQueryHandler()

    result = await handler.handle(
        GetTestQuery(
            identifier=100,
        ),
    )

    assert result == "100"