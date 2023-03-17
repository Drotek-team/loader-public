from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
import pytest
from hypothesis import example, given
from hypothesis import strategies as st
from loader.show_env.show_user.convex_hull import (
    AngleOutOfBoundsError,
    calculate_angle,
    calculate_convex_hull,
    cross_product,
    get_p0,
    sort_positions,
)

from tests.strategies import slow


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass(frozen=True)
class Segment:
    first_point: Point
    second_point: Point


def ccw(a: Point, b: Point, c: Point) -> bool:
    return (c.y - a.y) * (b.x - a.x) > (b.y - a.y) * (c.x - a.x)


# Return true if line segments AB and CD intersect
def points_intersect(a: Point, b: Point, c: Point, d: Point) -> bool:
    return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)


def is_point_inside_convex_polygon(point: Point, polygon: List[Point]) -> bool:
    if len(polygon) < 3:
        return True
    mean_polygon_point = Point(
        float(np.mean([p.x for p in polygon])),
        float(np.mean([p.y for p in polygon])),
    )
    point_segment = Segment(mean_polygon_point, point)
    polygon_segments = [
        Segment(first_polygon_point, second_polygon_point)
        for first_polygon_point, second_polygon_point in zip(polygon[1:], polygon[:-1])
    ]
    return not (
        any(
            points_intersect(
                point_segment.first_point,
                point_segment.second_point,
                polygon_segment.first_point,
                polygon_segment.second_point,
            )
            and not (
                ccw(
                    point_segment.second_point,
                    polygon_segment.first_point,
                    polygon_segment.second_point,
                )
            )
            for polygon_segment in polygon_segments
        )
    )


def from_tuple_to_point(tuple_input: Tuple[float, float]) -> Point:
    return Point(tuple_input[0], tuple_input[1])


def from_tuple_list_to_point_list(
    tuple_list_input: List[Tuple[float, float]],
) -> List[Point]:
    return [from_tuple_to_point(tuple_input) for tuple_input in tuple_list_input]


st_coordinate = st.floats(min_value=-100, max_value=100)
st_position = st.tuples(st_coordinate, st_coordinate)


@st.composite
def st_positions_tuple(draw: st.DrawFn) -> List[Tuple[float, float]]:
    positions_tuple = draw(st.lists(st_position, min_size=1, max_size=100))
    return list(
        {tuple(round(x, 3) for x in position) for position in positions_tuple},
    )


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
    convex_hull = calculate_convex_hull(positions_tuple)

    position_points = from_tuple_list_to_point_list(positions_tuple)
    convex_hull_points = from_tuple_list_to_point_list(convex_hull)
    assert all(
        is_point_inside_convex_polygon(position_point, convex_hull_points)
        for position_point in position_points
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
