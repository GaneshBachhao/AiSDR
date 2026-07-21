"""
Query Builder

Reusable SQLAlchemy query helpers.
"""

from sqlalchemy import or_
from sqlalchemy.orm import Query


class QueryBuilder:
    """
    Utility methods for building SQLAlchemy queries.
    """

    @staticmethod
    def paginate(
        query: Query,
        page: int,
        size: int,
    ) -> Query:
        """
        Apply pagination.
        """

        offset = (page - 1) * size

        return (
            query
            .offset(offset)
            .limit(size)
        )

    @staticmethod
    def search(
        query: Query,
        search: str,
        columns: list,
    ) -> Query:
        """
        Apply case-insensitive search across columns.
        """

        if not search:

            return query

        filters = [

            column.ilike(f"%{search}%")

            for column in columns

        ]

        return query.filter(
            or_(
                *filters,
            )
        )

    @staticmethod
    def order_by(
        query: Query,
        column,
        descending: bool = False,
    ) -> Query:
        """
        Apply sorting.
        """

        if descending:

            return query.order_by(
                column.desc(),
            )

        return query.order_by(
            column.asc(),
        )