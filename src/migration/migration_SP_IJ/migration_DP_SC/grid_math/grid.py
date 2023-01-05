from dataclasses import dataclass
from typing import List, Tuple

import numpy as np


@dataclass
class HorizontalPosition:
    drone_index: int
    x: float  # NED in meter
    y: float  # NED in meter

    @property
    def xy_array(self) -> np.ndarray:
        return np.array((self.x, self.y))

    @property
    def xy_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)

    def rotated_positions(self, rotation_matrix: np.ndarray) -> None:
        xy_array_rotated = rotation_matrix @ self.xy_array
        self.x, self.y = xy_array_rotated[0], xy_array_rotated[1]


def get_rotation_matrix(angle: float) -> np.ndarray:
    angle = np.radians(angle)
    c, s = np.cos(angle), np.sin(angle)
    return np.array(((c, -s), (s, c)))


# TO DO: make a list type for this one
class Grid:
    def __init__(self, horizontal_positions: List[Tuple[float, float]]):
        self.horizontal_positions = [
            HorizontalPosition(
                drone_index, horizontal_position[0], horizontal_position[1]
            )
            for drone_index, horizontal_position in enumerate(horizontal_positions)
        ]

    def __iter__(self):
        yield from self.horizontal_positions

    def __getitem__(self, horizontal_position_index: int) -> HorizontalPosition:
        if not (isinstance(horizontal_position_index, int)):
            raise ValueError("Only integer index are dealing by this function")
        return self.horizontal_positions[horizontal_position_index]

    def __len__(self):
        return len(self.horizontal_positions)

    def rotate_horizontal_positions(self, angle_rotation: float) -> None:
        rotation_matrix = get_rotation_matrix(angle_rotation)
        for horizontal_position in self.horizontal_positions:
            horizontal_position.rotated_positions(rotation_matrix)

    @property
    def horizontal_x_extremes(self) -> Tuple[HorizontalPosition, HorizontalPosition]:
        self.rotate_horizontal_positions(1e-3)
        ordered_horizontal_positions = sorted(
            self.horizontal_positions,
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
            self.horizontal_positions,
            key=lambda horizontal_position: horizontal_position.y,
        )
        self.rotate_horizontal_positions(-1e-3)
        return (
            ordered_horizontal_positions[0],
            ordered_horizontal_positions[-1],
        )
