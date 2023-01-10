from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
import pytest

from .show_px4 import DronePx4, ShowPx4


def generate_show_px4_from_first_position(
    first_positions: List[Tuple[int, int, int]]
) -> ShowPx4:
    drones = [DronePx4(drone_index) for drone_index in range(len(first_positions))]
    for first_position, drone in zip(first_positions, drones):
        drone.add_position(0, first_position)

    drone_center = DronePx4(len(first_positions))
    drone_center.add_position(0, (0, 0, 0))
    drones += [drone_center]

    return ShowPx4(drones)


@pytest.fixture
def valid_show_px4_list() -> List[ShowPx4]:
    nb_drones_manager = 10
    nb_drones_per_show_px4 = 100
    np.random.seed(42)
    return [
        generate_show_px4_from_first_position(
            [
                (
                    int(np.random.normal(scale=10)),
                    int(np.random.normal(scale=10)),
                    int(np.random.normal(scale=10)),
                )
                for _ in range(nb_drones_per_show_px4)
            ]
        )
        for _ in range(nb_drones_manager)
    ]


@dataclass(frozen=True)
class Point:
    x: int
    y: int


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
    point_segment = Segment(Point(0, 0), point)
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


def from_tuple_to_point(tuple_input: Tuple[int, int]) -> Point:
    return Point(tuple_input[0], tuple_input[1])


def from_tuple_list_to_point_list(
    tuple_list_input: List[Tuple[int, int]]
) -> List[Point]:
    return [from_tuple_to_point(tuple_input) for tuple_input in tuple_list_input]


def test_valid_convex_hull(valid_show_px4_list: List[ShowPx4]):
    assert all(
        is_point_inside_convex_polygon(
            from_tuple_to_point(horizontal_position),
            from_tuple_list_to_point_list(valid_show_px4.convex_hull),
        )
        for valid_show_px4 in valid_show_px4_list
        for horizontal_position in valid_show_px4.first_horizontal_positions
    )
