from app.domain.recommendation.entities.solution import Solution


def test_is_existing_offering_defaults_true():
    solution = Solution(title="X", description="Y", solution_type="Custom")
    assert solution.is_existing_offering is True


def test_is_existing_offering_can_be_set_false():
    solution = Solution(
        title="X", description="Y", solution_type="Custom", is_existing_offering=False
    )
    assert solution.is_existing_offering is False
