"""
Pagination Utilities
"""

from math import ceil

from app.schemas.common_schema import (
    PaginatedResponse,
)


class Pagination:

    @staticmethod
    def create(
        *,
        items,
        page: int,
        size: int,
        total_records: int,
    ) -> PaginatedResponse:

        total_pages = ceil(
            total_records / size
        ) if size else 0

        return PaginatedResponse(
            items=items,
            page=page,
            size=size,
            total_records=total_records,
            total_pages=total_pages,
        )