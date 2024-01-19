import hypothesis.strategies as st
from hypothesis import example, given
from loader.reports.ranges import get_drone_indices_from_ranges, get_ranges_from_drone_indices


def test_get_drone_indices_ranges() -> None:
    assert get_ranges_from_drone_indices({0, 2, 3, 4, 7, 8, 12, 13}) == "0,2-4,7-8,12-13"


@given(st.sets(st.integers(min_value=0)))
@example({0, 1, 3})
def test_get_drone_indices_from_ranges_get_ranges_from_drone_indices(
    drone_indices: set[int],
) -> None:
    assert (
        get_drone_indices_from_ranges(get_ranges_from_drone_indices(drone_indices)) == drone_indices
    )
