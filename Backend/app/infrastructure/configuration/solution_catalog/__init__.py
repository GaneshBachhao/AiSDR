"""
AI Solution Catalog loader.

Seed data lives in this directory as JSON, one file per sector (plus
``general.json`` for sector-agnostic existing offerings). Loading is a
pure infrastructure concern (file I/O) that produces the domain-layer
``SolutionCatalogEntry`` value object -- mirrors the
``app.infrastructure.configuration.domain_profiles`` loader pattern.
"""

from __future__ import annotations

import json
from pathlib import Path

from app.domain.recommendation.value_objects.solution_catalog_entry import (
    SolutionCatalogEntry,
)

_CATALOG_DIR = Path(__file__).parent


def _entry_from_dict(data: dict) -> SolutionCatalogEntry:
    return SolutionCatalogEntry(
        id=data["id"],
        sector=data["sector"],
        pain_point=data["pain_point"],
        solution_type=data["solution_type"],
        title=data["title"],
        description=data["description"],
        is_existing_offering=data["is_existing_offering"],
        signals=tuple(data.get("signals", ())),
    )


def load_solution_catalog() -> list[SolutionCatalogEntry]:
    """Load every seed entry across every sector file in this directory."""

    entries: list[SolutionCatalogEntry] = []

    for path in sorted(_CATALOG_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        entries.extend(_entry_from_dict(item) for item in data)

    return entries


def load_existing_offerings() -> list[SolutionCatalogEntry]:
    """Just the sector-agnostic, real Pamacore service-line entries."""

    return [entry for entry in load_solution_catalog() if entry.is_existing_offering]


__all__ = [
    "load_existing_offerings",
    "load_solution_catalog",
]
