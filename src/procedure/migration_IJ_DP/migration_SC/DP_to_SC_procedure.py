from dataclasses import dataclass
from ....drones_px4.drones_px4 import DronesPx4

from typing import Tuple
from ....iostar_json.show_configuration import ShowConfiguration
from typing import List
import numpy as np


@dataclass(frozen=True)
class HorizontalPosition:
    drone_index: int
    x: float
    y: float

    @property
    def xy_array(self) -> np.ndarray:
        return np.array((self.x, self.y))


def get_nb_drone_per_family_from_drones_px4(
    first_horizontal_positions: List[HorizontalPosition],
) -> int:
    first_horizontal_position_index_0 = first_horizontal_positions[0]
    if all(
        first_horizontal_position == first_horizontal_position_index_0
        for first_horizontal_position in first_horizontal_positions
    ):
        return 0
    for position_index, first_horizontal_position, first_horizontal_position_bis in zip(
        np.arange(1, len(first_horizontal_positions)),
        first_horizontal_positions[1:],
        first_horizontal_positions[:-1],
    ):
        if first_horizontal_position.x != first_horizontal_position_bis.x:
            return position_index
    return 0


def get_nb_x_nb_y_from_drones_px4(
    first_horizontal_positions: List[HorizontalPosition],
) -> Tuple[int, int]:
    first_horizontal_position_index_0 = first_horizontal_positions[0]
    if all(
        first_horizontal_position.xy_array == first_horizontal_position_index_0.xy_array
        for first_horizontal_position in first_horizontal_positions
    ):
        return 0, 0
    for position_index, first_horizontal_position, first_horizontal_position_bis in zip(
        np.arange(1, len(first_horizontal_positions)),
        first_horizontal_positions[1:],
        first_horizontal_positions[:-1],
    ):
        if first_horizontal_position.x != first_horizontal_position_bis.x:
            return position_index, len(first_horizontal_positions) // position_index
    return 0, 0


def get_step_from_drones_px4(
    first_horizontal_positions: List[HorizontalPosition],
) -> float:
    first_horizontal_position_index_0 = first_horizontal_positions[0]
    if all(
        np.array_equal(
            first_horizontal_position.xy_array,
            first_horizontal_position_index_0.xy_array,
        )
        for first_horizontal_position in first_horizontal_positions
    ):
        return 0
    for first_horizontal_position, first_horizontal_position_bis in zip(
        first_horizontal_positions[1:], first_horizontal_positions[:-1]
    ):
        if np.array_equal(
            first_horizontal_position.xy_array,
            first_horizontal_position_bis.xy_array,
        ):
            return np.linalg.norm(
                first_horizontal_position.xy_array
                - first_horizontal_position_bis.xy_array,
            )
    return 0.0


def get_popo(
    first_horizontal_positions: List[HorizontalPosition],
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray,]:
    sorted(
        first_horizontal_positions,
        key=lambda first_horizontal_position: tuple(first_horizontal_position.xy_array),
    )
    first_horizontal_position_x, last_horizontal_position_x = (
        first_horizontal_positions[0],
        first_horizontal_positions[-1],
    )

    sorted(
        first_horizontal_positions,
        key=lambda first_horizontal_position: tuple(
            reversed(first_horizontal_position.xy_array)
        ),
    )
    first_horizontal_position_y, last_horizontal_position_y = (
        first_horizontal_positions[0],
        first_horizontal_positions[-1],
    )
    return (
        np.array(first_horizontal_position_x),
        np.array(last_horizontal_position_x),
        np.array(first_horizontal_position_y),
        np.array(last_horizontal_position_y),
    )


def get_angle_from_vector(u_x: np.ndarray) -> float:
    u_x_unit = u_x / np.linalg.norm(u_x)
    return np.cos(u_x_unit[0])


def get_angle_takeoff_from_drones_px4(
    first_horizontal_positions: List[HorizontalPosition],
) -> float:
    (
        first_horizontal_position_x,
        last_horizontal_position_x,
        first_horizontal_position_y,
        last_horizontal_position_y,
    ) = get_popo(first_horizontal_positions)
    return get_angle_from_vector(
        last_horizontal_position_x - first_horizontal_position_x
    )


def get_rotation_matrix(angle: float) -> np.ndarray:
    angle = np.radians(angle)
    c, s = np.cos(angle), np.sin(angle)
    return np.array(((c, -s), (s, c)))


### TO DO: deal with the nb_drone = 0, nb_drone = 1 later
def DP_to_SC_procedure(drones_px4: DronesPx4) -> ShowConfiguration:
    horizontal_positions = [
        HorizontalPosition(
            drone_index, first_horizontal_position[0], first_horizontal_position[1]
        )
        for drone_index, first_horizontal_position in enumerate(
            drones_px4.first_horizontal_positions
        )
    ]
    angle_takeoff = get_angle_takeoff_from_drones_px4(horizontal_positions.copy())
    rotation_matrix = get_rotation_matrix(angle_takeoff)
    first_horizontal_positions_rotated = [
        rotation_matrix @ first_horizontal_position
        for first_horizontal_position in horizontal_positions
    ]
