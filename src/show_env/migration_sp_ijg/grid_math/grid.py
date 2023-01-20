import math
from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
import numpy.typing as npt

from ....show_env.show_user.show_user_generator import (
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
    def xy_array(self) -> npt.NDArray[np.float64]:
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
    def xy_array(self) -> npt.NDArray[np.float64]:
        return self.coordinate.xy_array

    @property
    def xy_tuple(self) -> Tuple[float, float]:
        return self.coordinate.xy_tuple


class Grid(List[HorizontalPosition]):
    def rotate_horizontal_positions(self, angle_radian: float) -> None:
        for horizontal_position in self:
            horizontal_position.rotated_positions(angle_radian)

    def is_grid_one_drone(self) -> bool:
        return len(self) == 1

    def is_grid_one_family(self) -> bool:
        return all(
            self[0].xy_tuple == horizontal_position.xy_tuple
            for horizontal_position in self[1:]
        )

    def get_corner_down_right_and_down_left(
        self, nb_drone_per_family: int
    ) -> Tuple[HorizontalPosition, HorizontalPosition]:
        if self.is_grid_one_drone() or len(self) == nb_drone_per_family:
            return (self[0], self[0])
        return (self[0], self[nb_drone_per_family])


# TODO: test this
def get_grid_from_show_user(show_user: ShowUser) -> Grid:
    return Grid(
        [
            HorizontalPosition(
                drone_index,
                Coordinate(horizontal_position[0], horizontal_position[1]),
            )
            for drone_index, horizontal_position in enumerate(
                show_user.first_horizontal_positions
            )
        ]
    )


# TODO: test this
def get_grid_from_configuration(grid_configuration: GridConfiguration) -> Grid:
    return get_grid_from_show_user(
        get_valid_show_user(
            ShowUserConfiguration(
                nb_x=grid_configuration.nb_x,
                nb_y=grid_configuration.nb_y,
                nb_drone_per_family=grid_configuration.nb_drone_per_family,
                step_takeoff=grid_configuration.step_takeoff,
                angle_takeoff=grid_configuration.angle_takeoff,
            )
        )
    )
