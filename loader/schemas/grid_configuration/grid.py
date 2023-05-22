from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING, List

import numpy as np

from loader.schemas.show_user import ShowUser
from loader.schemas.show_user.generate_show_user import get_valid_show_user

from .grid_configuration import GridConfiguration

if TYPE_CHECKING:
    from numpy.typing import NDArray


@dataclass(frozen=True)
class Coordinate:
    x: float  # ENU in meter
    y: float  # ENU in meter

    @property
    def xy_array(self) -> NDArray[np.float64]:
        return np.array((self.x, self.y), dtype=np.float64)

    @property
    def xy_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Coordinate):
            return False
        return np.allclose(self.xy_array, __o.xy_array, 1e-6)


@dataclass(unsafe_hash=True)
class HorizontalPosition:
    drone_index: int
    coordinate: Coordinate

    def rotated_positions(self, angle_radian: float) -> None:
        self.coordinate = Coordinate(
            self.coordinate.x * math.cos(angle_radian) - self.coordinate.y * math.sin(angle_radian),
            self.coordinate.x * math.sin(angle_radian) + self.coordinate.y * math.cos(angle_radian),
        )

    @property
    def x(self) -> float:
        return self.coordinate.x

    @property
    def y(self) -> float:
        return self.coordinate.y

    @property
    def xy_array(self) -> NDArray[np.float64]:
        return self.coordinate.xy_array

    @property
    def xy_tuple(self) -> tuple[float, float]:
        return self.coordinate.xy_tuple


ARBITRARY_ROUNDING_TOLERANCE = 1e-6


class Grid(List[HorizontalPosition]):
    def is_grid_one_drone(self) -> bool:
        return len(self) == 1

    def is_grid_one_family(self) -> bool:
        return all(
            self[0].xy_tuple == horizontal_position.xy_tuple for horizontal_position in self[1:]
        )

    def rotate_horizontal_positions(self, angle_radian: float) -> None:
        for horizontal_position in self:
            horizontal_position.rotated_positions(angle_radian)

    @classmethod
    def from_show_user(cls, show_user: ShowUser) -> Grid:
        return Grid(
            [
                HorizontalPosition(
                    drone_user.index,
                    Coordinate(
                        drone_user.first_horizontal_position[0],
                        drone_user.first_horizontal_position[1],
                    ),
                )
                for drone_user in show_user.drones_user
            ],
        )

    @classmethod
    def from_grid_configuration(cls, grid_configuration: GridConfiguration) -> Grid:
        return Grid.from_show_user(get_valid_show_user(grid_configuration))

    def get_first_and_second_family_horizontal_positions(
        self,
        nb_drone_per_family: int,
    ) -> tuple[HorizontalPosition, HorizontalPosition]:
        if self.is_grid_one_drone() or self.is_grid_one_family():
            return (self[0], self[0])
        return (self[0], self[nb_drone_per_family])

    @staticmethod
    def get_angle_degree_from_vector(u_x: NDArray[np.float64]) -> float:
        u_x_unit = u_x / np.linalg.norm(u_x)
        return np.arctan2(u_x_unit[1], u_x_unit[0])

    def get_angle_takeoff(
        self,
        nb_drone_per_family: int,
    ) -> float:
        if self.is_grid_one_drone() or self.is_grid_one_family():
            return 0.0
        (
            first_row_first_position,
            first_row_last_position,
        ) = self.get_first_and_second_family_horizontal_positions(nb_drone_per_family)
        return self.get_angle_degree_from_vector(
            first_row_last_position.xy_array - first_row_first_position.xy_array,
        )

    def get_nb_drone_per_family(self) -> int:
        for first_horizontal_position, second_horizontal_position in zip(self[:-1], self[1:]):
            if first_horizontal_position.xy_tuple != second_horizontal_position.xy_tuple:
                # Case where there are multiple families
                return second_horizontal_position.drone_index
        # Case where there is only one family
        return len(self)

    def get_nb_x_nb_y(
        self,
        nb_drone_per_family: int,
        angle_radian: float,
    ) -> tuple[int, int]:
        self.rotate_horizontal_positions(-angle_radian)
        for first_horizontal_position, second_horizontal_position in zip(self[:-1], self[1:]):
            if not np.allclose(
                first_horizontal_position.y,
                second_horizontal_position.y,
                rtol=ARBITRARY_ROUNDING_TOLERANCE,
            ):
                return (
                    second_horizontal_position.drone_index // nb_drone_per_family,
                    len(self) // (second_horizontal_position.drone_index),
                )
        self.rotate_horizontal_positions(angle_radian)
        return (len(self) // nb_drone_per_family, 1)

    def get_step(self) -> float:
        for first_horizontal_position, second_horizontal_position in zip(self[:-1], self[1:]):
            if first_horizontal_position.xy_tuple != second_horizontal_position.xy_tuple:
                return float(
                    np.linalg.norm(
                        first_horizontal_position.xy_array - second_horizontal_position.xy_array,
                    ),
                )
        return 0.0
