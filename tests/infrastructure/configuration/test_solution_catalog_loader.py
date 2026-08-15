from app.domain.recommendation.value_objects.solution_catalog_entry import (
    SolutionCatalogEntry,
)
from app.infrastructure.configuration.solution_catalog import (
    load_existing_offerings,
    load_solution_catalog,
)


def test_load_solution_catalog_returns_populated_entries():
    catalog = load_solution_catalog()
    assert len(catalog) > 25
    assert all(isinstance(entry, SolutionCatalogEntry) for entry in catalog)


def test_load_solution_catalog_covers_general_and_sector_entries():
    catalog = load_solution_catalog()
    sectors = {entry.sector for entry in catalog}
    assert "general" in sectors
    assert "manufacturing" in sectors
    assert "healthcare" in sectors


def test_load_existing_offerings_returns_only_flagged_entries():
    offerings = load_existing_offerings()
    assert offerings
    assert all(entry.is_existing_offering for entry in offerings)
    assert all(entry.sector == "general" for entry in offerings)


def test_generic_opportunities_are_never_flagged_as_existing_offerings():
    catalog = load_solution_catalog()
    generic = [entry for entry in catalog if entry.sector != "general"]
    assert generic
    assert all(not entry.is_existing_offering for entry in generic)


def test_entry_ids_are_unique():
    catalog = load_solution_catalog()
    ids = [entry.id for entry in catalog]
    assert len(ids) == len(set(ids))
