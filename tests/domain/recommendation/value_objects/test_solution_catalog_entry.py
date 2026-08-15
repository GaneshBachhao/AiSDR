from app.domain.recommendation.enums.solution_type import SolutionType
from app.domain.recommendation.value_objects.solution_catalog_entry import (
    SolutionCatalogEntry,
)


def _entry(**overrides) -> SolutionCatalogEntry:
    defaults = dict(
        id="x",
        sector="general",
        pain_point="Pain",
        solution_type="Custom",
        title="Title",
        description="Desc",
        is_existing_offering=True,
    )
    defaults.update(overrides)
    return SolutionCatalogEntry(**defaults)


def test_coerces_string_solution_type_to_enum():
    entry = _entry(solution_type="Chatbot")
    assert entry.solution_type == SolutionType.CHATBOT


def test_accepts_enum_solution_type_directly():
    entry = _entry(solution_type=SolutionType.ANALYTICS)
    assert entry.solution_type == SolutionType.ANALYTICS


def test_signals_default_to_empty_tuple():
    entry = _entry()
    assert entry.signals == ()


def test_is_frozen():
    entry = _entry()
    try:
        entry.title = "changed"
        assert False, "expected an error assigning to a frozen dataclass"
    except AttributeError:
        pass
