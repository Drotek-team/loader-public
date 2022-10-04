from multiprocessing.sharedctypes import Value
from typing import List, Tuple

import numpy as np


def get_relative_angle(origin: np.ndarray, coordinate: np.ndarray) -> float:
    vector = coordinate - origin
    u_vector = vector / np.linalg.norm(vector)
    return u_vector[0]


def sorted_by_pivot(positions: np.ndarray, pivot: np.ndarray) -> List[np.ndarray]:
    argsort = np.argsort(
        [get_relative_angle(pivot, position) for position in positions]
    )
    return list(positions[argsort])


def evaluate_pivot(positions: List[Tuple[int, int]]) -> Tuple[int, int]:
    return max(positions, key=lambda u: u[1])


def two_dimensionnal_cross_product(
    position_0: np.ndarray, position_1: np.ndarray, position_2: np.ndarray
) -> float:
    return (position_1[0] - position_0[0]) * (position_2[1] - position_0[1]) - (
        position_1[1] - position_0[1]
    ) * (position_2[0] - position_0[0])


### TO DO: Clean this algorithm, barely readable
def calculate_convex_hull(positions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Graham scan implementation"""
    pivot = evaluate_pivot(positions)
    positions.remove(pivot)
    convex_hull = [np.array(pivot)]
    convex_hull_tuple = [pivot]
    sorted_array_positions = sorted_by_pivot(np.array(positions), np.array(pivot))
    for sorted_array_position in sorted_array_positions:
        while (
            len(convex_hull) > 1
            and two_dimensionnal_cross_product(
                convex_hull[-1], convex_hull[-2], sorted_array_position
            )
            >= 0
        ):
            convex_hull.pop()
            convex_hull_tuple.pop()
        convex_hull.append(sorted_array_position)
        convex_hull_tuple.append(
            (int(sorted_array_position[0]), int(sorted_array_position[1]))
        )
    return convex_hull_tuple
