from __future__ import annotations

import pytest

from app.domain.qualification.value_objects.qualification_score import QualificationScore


def test_accepts_a_value_in_range() -> None:
    score = QualificationScore(75)

    assert score.value == 75
    assert score.percentage == 75


def test_accepts_the_boundary_values() -> None:
    assert QualificationScore(0).value == 0
    assert QualificationScore(100).value == 100


@pytest.mark.parametrize("value", [-1, 100.1, 250])
def test_rejects_out_of_range_values(value: float) -> None:
    with pytest.raises(ValueError):
        QualificationScore(value)


def test_is_immutable() -> None:
    score = QualificationScore(50)

    with pytest.raises(AttributeError):
        score.value = 60  # type: ignore[misc]


def test_equality_by_value() -> None:
    assert QualificationScore(42) == QualificationScore(42)
    assert QualificationScore(42) != QualificationScore(43)
