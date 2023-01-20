import math
from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
import numpy.typing as npt

from ....show_env.show_user.show_user_generator import get_valid_show_user
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

    # TODO: maybe there is a way to fuse these two methods
    def horizontal_x_extremes(
        self, nb_drone_per_family: int
    ) -> Tuple[HorizontalPosition, HorizontalPosition]:
        ordered_horizontal_positions = sorted(
            self,
            key=lambda horizontal_position: (
                horizontal_position.x,
                horizontal_position.drone_index,
            ),
        )
        return (
            ordered_horizontal_positions[nb_drone_per_family - 1],
            ordered_horizontal_positions[-1],
        )

    # TODO: maybe there is a way to fuse these two methods
    def horizontal_y_extremes(
        self, nb_drone_per_family: int
    ) -> Tuple[HorizontalPosition, HorizontalPosition]:
        ordered_horizontal_positions = sorted(
            self,
            key=lambda horizontal_position: (
                horizontal_position.y,
                horizontal_position.drone_index,
            ),
        )
        return (
            ordered_horizontal_positions[nb_drone_per_family - 1],
            ordered_horizontal_positions[-1],
        )

    def is_grid_one_drone(self) -> bool:
        return len(self) == 1

    # TODO: test these methods
    def is_grid_one_family(self) -> bool:
        return all(
            self[0].xy_tuple == horizontal_position.xy_tuple
            for horizontal_position in self[1:]
        )

    def is_grid_a_row(self, nb_drone_per_family: int) -> bool:
        return set(self.horizontal_x_extremes(nb_drone_per_family)) == set(
            self.horizontal_y_extremes(nb_drone_per_family)
        )

    # TODO: get corners are useless, all you need to do is know the number of family and jump to the next one
    def get_corner_down_right_and_down_left(
        self, nb_drone_per_family: int
    ) -> Tuple[HorizontalPosition, HorizontalPosition]:
        self.rotate_horizontal_positions(1e-3)
        corners = list(self.horizontal_x_extremes(nb_drone_per_family)) + list(
            self.horizontal_y_extremes(nb_drone_per_family)
        )
        enu_sorted_corners = sorted(
            corners,
            key=lambda corner: corner.drone_index,
        )
        if self.is_grid_a_row(nb_drone_per_family):
            return (enu_sorted_corners[0], enu_sorted_corners[-1])
        return (
            enu_sorted_corners[0],
            enu_sorted_corners[1],
        )


@dataclass(frozen=True)
class GridConfiguration:
    nb_x: int = 1
    nb_y: int = 1
    nb_drone_per_family: int = 1
    step_takeoff: float = 1.5
    angle_takeoff: float = 0.0


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
            grid_configuration.nb_x,
            grid_configuration.nb_y,
            grid_configuration.nb_drone_per_family,
            grid_configuration.step_takeoff,
            grid_configuration.angle_takeoff,
        )
    )
