from typing import List, Tuple

import numpy as np


def get_relative_angle(origin: np.ndarray, coordinate: np.ndarray) -> float:
    vector = coordinate - origin
    u_vector = vector / np.linalg.norm(vector)
    return u_vector[0]


def sorted_by_pivot(positions: List[np.ndarray], pivot: np.ndarray) -> np.ndarray:
    argsort = np.argsort(
        [get_relative_angle(pivot, position) for position in positions]
    )
    return positions[argsort]


def evaluate_pivot(positions: List[np.ndarray]) -> np.ndarray:
    return max(positions, key=lambda u: u[1])


def two_dimensionnal_cross_product(
    position_0: np.ndarray, position_1: np.ndarray, position_2: np.ndarray
) -> float:
    return (position_1[0] - position_0[0]) * (position_2[1] - position_0[1]) - (
        position_1[1] - position_0[1]
    ) * (position_2[0] - position_0[0])


### TO DO: Clean this typing thing
def calculate_convex_hull(positions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Graham scan implementation"""
    pivot = evaluate_pivot(positions)
    positions.remove(pivot)
    convex_hull = [pivot]
    positions_array = np.array(positions)
    sorted_array_positions = sorted_by_pivot(positions_array, pivot)
    for sorted_array_position in sorted_array_positions:
        while (
            len(convex_hull) > 1
            and two_dimensionnal_cross_product(
                convex_hull[-1], convex_hull[-2], sorted_array_position
            )
            >= 0
        ):
            convex_hull.pop()
        convex_hull.append(sorted_array_position)
    convex_hull = [tuple(point) for point in convex_hull]
    return convex_hull
