from typing import List, Tuple

import pytest
from hypothesis import assume, example, given
from hypothesis import strategies as st
from loader.schemas.show_user.convex_hull import (
    AngleOutOfBoundsError,
    calculate_angle,
    calculate_convex_hull,
    cross_product,
    get_p0,
    sort_positions,
)
from shapely.geometry.polygon import Polygon  # pyright: ignore[reportUnknownVariableType]

from tests.strategies import slow

st_coordinate = st.floats(min_value=-100, max_value=100)
st_position = st.tuples(st_coordinate, st_coordinate)


@st.composite
def st_positions_tuple(draw: st.DrawFn) -> List[Tuple[float, float]]:
    positions_tuple = draw(st.lists(st_position, min_size=1, max_size=100))
    # assume that all points are not collinear
    if len(positions_tuple) >= 3:
        assume(
            all(  # pragma: no cover
                cross_product(p1, p2, p3) != 0
                for i, p1 in enumerate(positions_tuple)
                for j, p2 in enumerate(positions_tuple)
                for k, p3 in enumerate(positions_tuple)
                if i != j != k
            ),
        )
    return positions_tuple


@given(positions_tuple=st_positions_tuple())
@example(positions_tuple=[(0.0, 0.0), (0.0, 1.0), (1.0, 0.0)])
@example(
    [
        (1, 0),
        (2, 0),
        (4, 2),
        (2, 1),
        (-2, 2),
        (1, 1),
        (1, 2),
        (-2, 1),
        (2, 2),
        (2, 4),
        (0, 2),
        (0, 1),
        (0, 0),
        (-2, 4),
        (-1, 2),
        (-1, 1),
        (-4, 2),
    ],
)
@example([(2, 2), (1, 2), (-2, 2), (0, 0), (2, -2), (-2, -2), (-1, -2)])
@example(
    [
        (-236, -209),
        (-136, -36),
        (-36, 136),
        (63, 309),
        (-63, -309),
        (36, -136),
        (136, 36),
        (236, 209),
    ],
)
@slow
def test_calculate_convex_hull(positions_tuple: List[Tuple[float, float]]) -> None:
    calculated_convex_hull = calculate_convex_hull(positions_tuple)
    if len(positions_tuple) < 3:
        assert set(calculated_convex_hull) == set(positions_tuple)
        return
    assert Polygon(calculated_convex_hull).equals(  # pyright: ignore[reportUnknownMemberType]
        Polygon(
            positions_tuple,
        ).convex_hull,  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
    )


@pytest.mark.parametrize(
    "positions, p0",
    [
        ([(0, 0), (-1, 1), (0, 1)], (0, 0)),
        ([(-2, 3), (-5, 8), (4, -2), (7, -2)], (4, -2)),
    ],
)
def test_get_p0(positions: List[Tuple[float, float]], p0: Tuple[float, float]) -> None:
    assert get_p0(positions) == p0
    assert get_p0(reversed(positions)) == p0


@pytest.mark.parametrize(
    "p0, p, expected",
    [
        ((0, 0), (0, 0), (float("-inf"), 0)),
        ((0, 0), (1, 0), (float("-inf"), 1)),
        ((0, 0), (2, 0), (float("-inf"), 2)),
        ((0, 0), (2, 1), (-2, 1)),
        ((0, 0), (4, 2), (-2, 2)),
        ((0, 0), (1, 1), (-1, 1)),
        ((0, 0), (2, 2), (-1, 2)),
        ((0, 0), (1, 2), (-0.5, 2)),
        ((0, 0), (2, 4), (-0.5, 4)),
        ((0, 0), (0, 1), (0, 1)),
        ((0, 0), (0, 2), (0, 2)),
        ((0, 0), (-1, 2), (0.5, 2)),
        ((0, 0), (-2, 4), (0.5, 4)),
        ((0, 0), (-1, 1), (1, 1)),
        ((0, 0), (-2, 2), (1, 2)),
        ((0, 0), (-2, 1), (2, 1)),
        ((0, 0), (-4, 2), (2, 2)),
        ((-1, -1), (-1, -1), (float("-inf"), 0)),
        ((-1, -1), (1, -1), (float("-inf"), 2)),
        ((-1, -1), (0, 0), (-1, 1)),
        ((-1, -1), (-1, 1), (0, 2)),
        ((-1, -1), (-2, 0), (1, 1)),
    ],
)
def test_calculate_angle(
    p0: Tuple[float, float],
    p: Tuple[float, float],
    expected: Tuple[float, int],
) -> None:
    assert calculate_angle(p0, p) == expected


@pytest.mark.parametrize(
    "p0, p",
    [
        ((0, 0), (-1, 0)),
        ((0, 0), (-1, -1)),
        ((0, 0), (0, -2)),
        ((0, 0), (1, -1)),
        ((1, 0), (0, 0)),
        ((0, 1), (-1, 0)),
        ((-1, -1), (-1, -3)),
        ((-2, 0), (-1, -1)),
    ],
)
def test_calculate_angle_out_of_bounds(
    p0: Tuple[float, float],
    p: Tuple[float, float],
) -> None:
    with pytest.raises(AngleOutOfBoundsError):
        calculate_angle(p0, p)


@pytest.mark.parametrize(
    "positions, sorted_positions",
    [
        (
            [
                (1, 0),
                (2, 0),
                (4, 2),
                (2, 1),
                (-2, 2),
                (1, 1),
                (1, 2),
                (-2, 1),
                (2, 2),
                (2, 4),
                (0, 2),
                (0, 1),
                (0, 0),
                (-2, 4),
                (-1, 2),
                (-1, 1),
                (-4, 2),
            ],
            [
                (0, 0),
                (1, 0),
                (2, 0),
                (2, 1),
                (4, 2),
                (1, 1),
                (2, 2),
                (1, 2),
                (2, 4),
                (0, 1),
                (0, 2),
                (-1, 2),
                (-2, 4),
                (-1, 1),
                (-2, 2),
                (-2, 1),
                (-4, 2),
            ],
        ),
        (
            [(2, 2), (1, 2), (-2, 2), (0, 0), (2, -2), (-2, -2), (-1, -2)],
            [(-2, -2), (-1, -2), (2, -2), (0, 0), (2, 2), (1, 2), (-2, 2)],
        ),
    ],
)
def test_sort_positions(
    positions: List[Tuple[float, float]],
    sorted_positions: List[Tuple[float, float]],
) -> None:
    assert sort_positions(positions) == sorted_positions


def test_cross_product() -> None:
    assert (
        cross_product(
            (0, 0),
            (1, 0),
            (0, 1),
        )
        > 0
    )
    assert (
        cross_product(
            (1, 0),
            (2, 0),
            (3, 0),
        )
        == 0
    )
    assert (
        cross_product(
            (0, -1),
            (0, -2),
            (-1, -1),
        )
        < 0
    )


@pytest.mark.parametrize(
    "positions, convex_hull",
    [
        (
            [
                (1, 0),
                (2, 0),
                (4, 2),
                (2, 1),
                (-2, 2),
                (1, 1),
                (1, 2),
                (-2, 1),
                (2, 2),
                (2, 4),
                (0, 2),
                (0, 1),
                (0, 0),
                (-2, 4),
                (-1, 2),
                (-1, 1),
                (-4, 2),
            ],
            [(0, 0), (2, 0), (4, 2), (2, 4), (-2, 4), (-4, 2)],
        ),
        (
            [(2, 2), (1, 2), (-2, 2), (0, 0), (2, -2), (-2, -2), (-1, -2)],
            [(-2, -2), (2, -2), (2, 2), (-2, 2)],
        ),
        (
            [
                (-236, -209),
                (-136, -36),
                (-36, 136),
                (63, 309),
                (-63, -309),
                (36, -136),
                (136, 36),
                (236, 209),
            ],
            [(-63, -309), (236, 209), (63, 309), (-236, -209)],
        ),
    ],
)
def test_calculate_convex_hull_(
    positions: List[Tuple[float, float]],
    convex_hull: List[Tuple[float, float]],
) -> None:
    assert calculate_convex_hull(positions) == convex_hull
