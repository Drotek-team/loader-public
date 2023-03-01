import re
from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
import pytest
from hypothesis import example, given
from hypothesis import strategies as st
from loader.show_env.show_user.convex_hull import (
    calculate_convex_hull,
    get_relative_angle,
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
@slow
def test_calculate_convex_hull(positions_tuple: List[Tuple[float, float]]) -> None:
    convex_hull = calculate_convex_hull(positions_tuple)

    position_points = from_tuple_list_to_point_list(positions_tuple)
    convex_hull_points = from_tuple_list_to_point_list(convex_hull)
    assert all(
        is_point_inside_convex_polygon(position_point, convex_hull_points)
        for position_point in position_points
    )


def test_get_relative_angle_origin_equal_coordinate() -> None:
    with pytest.raises(
        ValueError,
        match=re.escape("get_relative_angle(): origin is equal to coordinate"),
    ):
        get_relative_angle(np.zeros(3), np.zeros(3))
