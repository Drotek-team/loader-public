import math
from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Tuple

import numpy as np

from loader.schemas.show_user import ShowUser
from loader.schemas.show_user.generate_show_user import get_valid_show_user

if TYPE_CHECKING:
    from numpy.typing import NDArray

    from .grid_configuration import GridConfiguration


@dataclass(frozen=True)
class Coordinate:
    x: float  # ENU in meter
    y: float  # ENU in meter

    @property
    def xy_array(self) -> "NDArray[np.float64]":
        return np.array((self.x, self.y), dtype=np.float64)

    @property
    def xy_tuple(self) -> Tuple[float, float]:
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
    def xy_array(self) -> "NDArray[np.float64]":
        return self.coordinate.xy_array

    @property
    def xy_tuple(self) -> Tuple[float, float]:
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
    def from_show_user(cls, show_user: ShowUser) -> "Grid":
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
    def from_grid_configuration(cls, grid_configuration: "GridConfiguration") -> "Grid":
        return Grid.from_show_user(get_valid_show_user(grid_configuration))

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
    ) -> Tuple[int, int]:
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
