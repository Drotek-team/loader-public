from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
import pytest

from .drones_px4 import DronePx4, DronesPx4


def generate_drones_px4_from_first_position(
    first_positions: List[Tuple[int, int, int]]
) -> DronesPx4:
    drones = [DronePx4(drone_index) for drone_index in range(len(first_positions))]
    for first_position, drone in zip(first_positions, drones):
        drone.add_position(0, first_position)

    drone_center = DronePx4(len(first_positions))
    drone_center.add_position(0, (0, 0, 0))
    drones += [drone_center]

    return DronesPx4(drones)


@pytest.fixture
def valid_drones_px4_list() -> List[DronesPx4]:
    NB_DRONES_MANAGER = 10
    nb_drones_per_drones_px4 = 100
    np.random.seed(42)
    return [
        generate_drones_px4_from_first_position(
            [
                (
                    int(np.random.normal(scale=10)),
                    int(np.random.normal(scale=10)),
                    int(np.random.normal(scale=10)),
                )
                for _ in range(nb_drones_per_drones_px4)
            ]
        )
        for _ in range(NB_DRONES_MANAGER)
    ]


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class Segment:
    first_point: Point
    second_point: Point


def ccw(A: Point, B: Point, C: Point) -> bool:
    return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)


# Return true if line segments AB and CD intersect
def points_intersect(A: Point, B: Point, C: Point, D: Point) -> bool:
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


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


### TO DO: add hypothesis/strategies to these tests
def test_valid_convex_hull(valid_drones_px4_list: List[DronesPx4]):
    assert all(
        is_point_inside_convex_polygon(
            from_tuple_to_point(horizontal_position),
            from_tuple_list_to_point_list(valid_drones_px4.convex_hull),
        )
        for valid_drones_px4 in valid_drones_px4_list
        for horizontal_position in valid_drones_px4.first_horizontal_positions
    )
