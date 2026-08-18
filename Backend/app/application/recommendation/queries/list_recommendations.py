from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ListRecommendationsQuery:
    page: int = 1
    page_size: int = 10
