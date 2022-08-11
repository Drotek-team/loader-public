from math import radians

import numpy as np
from typing import Tuple


class FamilyManager:
    def __init__(
        self,
        nb_x: int,
        nb_y: int,
        nb_drone_per_family: int,
        step_takeoff: int,
        angle_takeoff: int,
        show_duration_second: int,
        altitude_range_meter: Tuple[int, int],
    ):
        self.nb_x = nb_x
        self.nb_y = nb_y
        self.nb_drone_per_family = nb_drone_per_family
        self.step_takeoff = step_takeoff
        self.angle_takeoff = angle_takeoff
        self.show_duration_second = show_duration_second
        self.altitude_range_meter = altitude_range_meter

    @property
    def nb_family(self) -> int:
        return self.nb_x * self.nb_y

    def get_family_index(self, row_index: int, column_index: int) -> int:
        return self.nb_y * row_index + column_index

    def get_drone_index(self, family_index: int, family_drone_index: int) -> int:
        return self.nb_drone_per_family * family_index + family_drone_index

    @property
    def theorical_grid(self) -> np.ndarray:
        unrotate_theorical_position = np.array(
            [
                [
                    self.step_takeoff * (index_x - (self.nb_x - 1) / 2),
                    self.step_takeoff * (index_y - (self.nb_y - 1) / 2),
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
