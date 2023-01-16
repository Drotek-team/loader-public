from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
import numpy.typing as npt


@dataclass
class HorizontalPosition:
    drone_index: int
    x: float  # NED in meter
    y: float  # NED in meter

    def __hash__(self) -> int:
        return self.drone_index

    @property
    def xy_array(self) -> npt.NDArray[np.float64]:
        return np.array((self.x, self.y))

    @property
    def xy_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)

    def rotated_positions(self, rotation_matrix: npt.NDArray[np.float64]) -> None:
        xy_array_rotated = rotation_matrix @ self.xy_array
        self.x, self.y = xy_array_rotated[0], xy_array_rotated[1]


def get_rotation_matrix(angle: float) -> npt.NDArray[np.float64]:
    angle = np.radians(angle)
    c, s = np.cos(angle), np.sin(angle)
    return np.array(((c, -s), (s, c)))


class Grid(List[HorizontalPosition]):
    def rotate_horizontal_positions(self, angle_rotation: float) -> None:
        rotation_matrix = get_rotation_matrix(angle_rotation)
        for horizontal_position in self:
            horizontal_position.rotated_positions(rotation_matrix)

    @property
    def horizontal_x_extremes(self) -> Tuple[HorizontalPosition, HorizontalPosition]:
        self.rotate_horizontal_positions(1e-3)
        ordered_horizontal_positions = sorted(
            self,
            key=lambda horizontal_position: horizontal_position.x,
        )
        self.rotate_horizontal_positions(-1e-3)
        return (
            ordered_horizontal_positions[0],
            ordered_horizontal_positions[-1],
        )

    @property
    def horizontal_y_extremes(self) -> Tuple[HorizontalPosition, HorizontalPosition]:
        self.rotate_horizontal_positions(1e-3)
        ordered_horizontal_positions = sorted(
            self,
            key=lambda horizontal_position: horizontal_position.y,
        )
        self.rotate_horizontal_positions(-1e-3)
        return (
            ordered_horizontal_positions[0],
            ordered_horizontal_positions[-1],
        )


def get_grid_from_horizontal_positions(positions: List[Tuple[float, float]]):
    return Grid(
        [
            HorizontalPosition(
                drone_index,
                horizontal_position[0],
                horizontal_position[1],
            )
            for drone_index, horizontal_position in enumerate(positions)
        ]
    )
