from math import ceil
from typing import Any

from pydantic import BaseModel


class PaginationMetadata(BaseModel):
    page: int
    size: int
    total_records: int
    total_pages: int
    has_next: bool
    has_previous: bool


class PaginatedResponse(BaseModel):
    items: list[Any]
    pagination: PaginationMetadata

    @staticmethod
    def create(
        items: list[Any],
        page: int,
        size: int,
        total_records: int,
    ):
        total_pages = ceil(total_records / size) if total_records else 0

        return PaginatedResponse(
            items=items,
            pagination=PaginationMetadata(
                page=page,
                size=size,
                total_records=total_records,
                total_pages=total_pages,
                has_next=page < total_pages,
                has_previous=page > 1,
            ),
        )