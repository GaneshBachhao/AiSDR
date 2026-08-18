# app/application/common/dto/paged_result.py

"""
Pagination DTO support.
"""

from __future__ import annotations

from typing import Generic, TypeVar

from app.application.common.dto.base_dto import BaseDTO

T = TypeVar("T")


class PagedResult(BaseDTO, Generic[T]):
    """
    Represents paginated application results.
    """

    items: list[T]

    page_number: int

    page_size: int

    total_items: int

    @property
    def total_pages(self) -> int:
        """
        Calculate total available pages.
        """
        if self.total_items == 0:
            return 0

        return (self.total_items + self.page_size - 1) // self.page_size
