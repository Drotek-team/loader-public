from dataclasses import dataclass
from typing import Tuple, List
import numpy as np


@dataclass
class HorizontalPosition:
    drone_index: int
    x: float  # NED in meter
    y: float  # NED in meter

    @property
    def xy_array(self) -> np.ndarray:
        return np.array((self.x, self.y))

    def rotated_positions(self, rotation_matrix: np.ndarray) -> None:
        xy_array_rotated = rotation_matrix @ self.xy_array
        self.x, self.y = xy_array_rotated[0], xy_array_rotated[1]


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


### TO DO: A bit long for not clear reason
def get_popo(
    first_horizontal_positions: List[HorizontalPosition],
) -> Tuple[HorizontalPosition, HorizontalPosition]:
    sorted(
        first_horizontal_positions,
        key=lambda first_horizontal_position: tuple(first_horizontal_position.xy_array),
    )
    extreme_horizontal_positions: List[HorizontalPosition]
    extreme_horizontal_positions += [
        first_horizontal_positions[0],
        first_horizontal_positions[-1],
    ]

    sorted(
        first_horizontal_positions,
        key=lambda first_horizontal_position: tuple(
            reversed(first_horizontal_position.xy_array)
        ),
    )
    extreme_horizontal_positions += [
        first_horizontal_positions[0],
        first_horizontal_positions[-1],
    ]
    sorted(
        extreme_horizontal_positions,
        key=lambda extreme_horizontal_position: extreme_horizontal_position.drone_index,
    )
    return extreme_horizontal_positions[0], extreme_horizontal_positions[1]


def get_angle_from_vector(u_x: np.ndarray) -> float:
    u_x_unit = u_x / np.linalg.norm(u_x)
    return np.cos(u_x_unit[0])


def rotated_horizontal_positions(
    horizontal_positions: List[HorizontalPosition], angle_rotation: float
) -> None:
    rotation_matrix = get_rotation_matrix(angle_rotation)
    for horizontal_position in horizontal_positions:
        horizontal_position.rotated_positions(rotation_matrix)


def get_angle_takeoff_from_drones_px4(
    first_horizontal_positions: List[HorizontalPosition],
) -> float:
    (
        first_horizontal_position_x,
        last_horizontal_position_x,
    ) = get_popo(first_horizontal_positions)
    return get_angle_from_vector(
        last_horizontal_position_x.xy_array - first_horizontal_position_x.xy_array
    )


def get_rotation_matrix(angle: float) -> np.ndarray:
    angle = np.radians(angle)
    c, s = np.cos(angle), np.sin(angle)
    return np.array(((c, -s), (s, c)))
