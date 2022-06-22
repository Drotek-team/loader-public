from math import atan2, degrees
from typing import List

import numpy as np


class FamilyManager:
    def __init__(self, nb_x: int, nb_y: int, step: float):
        self.nb_x = nb_x
        self.nb_y = nb_y
        self.step = step
        self.rows: List[List[int]] = [[0 for _ in range(nb_y)] for _ in range(nb_x)]

    def get_family_index(self, row_index: int, column_index: int) -> int:
        return self.nb_y * row_index + column_index

    def get_nb_drone_per_row(self, row_index: int):
        return sum(self.rows[row_index])

    @staticmethod
    def get_angle(
        first_position: np.ndarray,
        second_position: np.ndarray,
        offset_radians: float = 0,
    ) -> int:
        u = second_position - first_position
        u = u / np.linalg.norm(u)
        return int(degrees(atan2(u[0], u[1]) + offset_radians))

    def angle_takeoff_degree(self, first_positions: List[np.ndarray]) -> int:
        if len(self.rows) == 1 and len(self.rows[0]) == 1:
            return 0
        find_angle = False
        row_index = 0
        while not (find_angle) and row_index < len(self.rows):
            if len(self.rows[row_index]) > 1:
                angle = self.get_angle(
                    np.array(first_positions[self.get_family_index(row_index, 0)]),
                    np.array(first_positions[self.get_family_index(row_index, 1)]),
                )
            row_index += 1
        if find_angle:
            return angle
        return self.get_angle(
            np.array(first_positions[self.get_family_index(0, 0)]),
            np.array(first_positions[self.get_family_index(1, 0)]),
            0.5 * np.pi,
        )
