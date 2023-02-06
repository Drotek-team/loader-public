import math
from dataclasses import dataclass
from typing import Any, List, Tuple

import numpy as np

from ...show_user.generate_show_user import (
    GridConfiguration,
    ShowUserConfiguration,
    get_valid_show_user,
)
from ...show_user.show_user import ShowUser


@dataclass(frozen=True)
class Coordinate:
    x: float  # ENU in meter
    y: float  # ENU in meter

    @property
    def xy_array(self) -> Any:
        return np.array((self.x, self.y))

    @property
    def xy_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Coordinate):
            return bool(np.linalg.norm(self.xy_array - __o.xy_array) < 1e-6)
        return False


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
    def xy_array(self) -> Any:
        return self.coordinate.xy_array

    @property
    def xy_tuple(self) -> Tuple[float, float]:
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
        ]
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
            )
        )
    )
