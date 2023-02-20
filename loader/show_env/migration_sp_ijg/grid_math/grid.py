from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING, List

import numpy as np

from loader.show_env.show_user import ShowUser
from loader.show_env.show_user.generate_show_user import (
    GridConfiguration,
    ShowUserConfiguration,
    get_valid_show_user,
)

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
            self.coordinate.x * math.cos(angle_radian)
            - self.coordinate.y * math.sin(angle_radian),
            self.coordinate.x * math.sin(angle_radian)
            + self.coordinate.y * math.cos(angle_radian),
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


class Grid(List[HorizontalPosition]):
    def is_grid_one_drone(self) -> bool:
        return len(self) == 1

    def is_grid_one_family(self) -> bool:
        return all(
            self[0].xy_tuple == horizontal_position.xy_tuple
            for horizontal_position in self[1:]
        )

    def rotate_horizontal_positions(self, angle_radian: float) -> None:
        for horizontal_position in self:
            horizontal_position.rotated_positions(angle_radian)


def get_grid_from_show_user(show_user: ShowUser) -> Grid:
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


def get_grid_from_configuration(grid_configuration: GridConfiguration) -> Grid:
    return get_grid_from_show_user(
        get_valid_show_user(
            ShowUserConfiguration(
                nb_x=grid_configuration.nb_x,
                nb_y=grid_configuration.nb_y,
                nb_drone_per_family=grid_configuration.nb_drone_per_family,
                step=grid_configuration.step,
                angle_takeoff=grid_configuration.angle_takeoff,
            ),
        ),
    )
