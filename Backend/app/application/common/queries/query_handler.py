# app/application/common/queries/query_handler.py

"""
Query handler contract.

Each query should have exactly one handler responsible for
retrieving application data.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar


TQuery = TypeVar(
    "TQuery",
)

TResult = TypeVar(
    "TResult",
)


class QueryHandler(
    ABC,
    Generic[TQuery, TResult],
):
    """
    Base query handler contract.
    """

    @abstractmethod
    async def handle(
        self,
        query: TQuery,
    ) -> TResult:
        """
        Execute the query.
        """
        raise NotImplementedError