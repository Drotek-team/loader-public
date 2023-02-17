import re
from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st
from loader.show_env.show_user.convex_hull import (
    calculate_convex_hull,
    get_relative_angle,
)


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


@given(nb_points=st.integers(2, 100))
def test_calculate_convex_hull(nb_points: int) -> None:
    positions_array = np.random.random((nb_points, 2))
    positions_tuple = [
        (float(position_array[0]), float(position_array[1]))
        for position_array in positions_array
    ]
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
