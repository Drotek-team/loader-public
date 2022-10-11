from dataclasses import dataclass
from typing import List, Tuple
from math import radians
import numpy as np


@dataclass(frozen=True)
class ShowConfiguration:
    nb_x: int  # Number of families on the x-axis during the takeoff
    nb_y: int  # Number of families on the y-axis during the takeoff
    nb_drone_per_family: int  # Number of drones in each families
    step: int  # Distance separating the families during the takeoff in centimeter
    angle_takeoff: int  # Angle of the takeoff grid in degree
    duration: float  # Duration of the show in second
    hull: List[
        Tuple[float, float]
    ]  # List of the relative coordinate (XY in ENU and meter) symbolysing a convex hull of a show
    altitude_range: Tuple[
        float, float
    ]  # Relative coordinate ( z_min and z_max in ENU and meter) symbolising the range of the z-axis

    @property
    def nb_family(self) -> int:
        return self.nb_x * self.nb_y

    def get_family_index(self, row_index: int, column_index: int) -> int:
        return self.nb_y * row_index + column_index

    def get_drone_index(self, family_index: int, family_drone_index: int) -> int:
        return self.nb_drone_per_family * family_index + family_drone_index

    @property
    def theorical_grid_from_parameter(self) -> np.ndarray:
        unrotate_theorical_position = np.array(
            [
                [
                    self.step * (index_x - (self.nb_x - 1) / 2),
                    self.step * (index_y - (self.nb_y - 1) / 2),
                ]
                for index_x in range(self.nb_x)
                for index_y in range(self.nb_y)
                for _ in range(self.nb_drone_per_family)
            ]
        )
        angle_radian = radians(self.angle_takeoff)
        rotation_matrix = np.array(
            [
                [np.cos(angle_radian), -np.sin(angle_radian)],
                [np.sin(angle_radian), np.cos(angle_radian)],
            ]
        )
        return unrotate_theorical_position @ rotation_matrix
