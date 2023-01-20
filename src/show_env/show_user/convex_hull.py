from typing import List, Tuple

import numpy as np
import numpy.typing as npt


def get_relative_angle(
    origin: npt.NDArray[np.float64], coordinate: npt.NDArray[np.float64]
) -> float:
    if np.array_equal(origin, coordinate):
        msg = "get_relative_angle(): origin is equal to coordinate"
        raise ValueError(msg)
    vector = coordinate - origin
    u_vector = vector / np.linalg.norm(vector)
    return u_vector[0]


def sorted_by_pivot(
    positions: npt.NDArray[np.float64], pivot: npt.NDArray[np.float64]
) -> List[npt.NDArray[np.float64]]:
    argsort = np.argsort(
        [get_relative_angle(pivot, position) for position in positions]
    )
    return list(positions[argsort])


def evaluate_pivot(positions: List[npt.NDArray[np.float64]]) -> npt.NDArray[np.float64]:
    return max(positions, key=lambda u: u[1])


def two_dimensionnal_cross_product(
    position_0: npt.NDArray[np.float64],
    position_1: npt.NDArray[np.float64],
    position_2: npt.NDArray[np.float64],
) -> float:
    return (position_1[0] - position_0[0]) * (position_2[1] - position_0[1]) - (
        position_1[1] - position_0[1]
    ) * (position_2[0] - position_0[0])


def tuple_list_to_array_list(
    tuple_list: List[Tuple[float, float]]
) -> List[npt.NDArray[np.float64]]:
    return [np.array(tuple_element) for tuple_element in tuple_list]


def array_list_to_tuple_list(
    array_list: List[npt.NDArray[np.float64]],
) -> List[Tuple[float, float]]:
    return [
        (float(array_element[0]), float(array_element[1]))
        for array_element in array_list
    ]


def calculate_convex_hull(
    positions_tuple: List[Tuple[float, float]]
) -> List[Tuple[float, float]]:
    """Graham scan implementation."""
    # IMPROVE: make an object with (index,tuple,array)
    positions_array = tuple_list_to_array_list(positions_tuple)

    # Begin Algorithm #
    pivot = evaluate_pivot(positions_array)
    # remove() does not work with list of array
    positions_array = [
        position_array
        for position_array in positions_array
        if not (np.array_equal(position_array, pivot))
    ]
    convex_hull = [pivot]
    sorted_array_positions = sorted_by_pivot(np.array(positions_array), np.array(pivot))
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
    # End algorithm ##

    return array_list_to_tuple_list(convex_hull)
