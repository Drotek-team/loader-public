from math import radians

import numpy as np


class FamilyManager:
    def __init__(self, nb_x: int, nb_y: int, step: float, angle: int):
        self.nb_x = nb_x
        self.nb_y = nb_y
        self.step = step
        self.angle = angle

    def get_family_index(self, row_index: int, column_index: int) -> int:
        return self.nb_y * row_index + column_index

    @property
    def theorical_grid(self) -> np.ndarray:
        unrotate_theorical_position = np.array(
            [
                self.step * (index_x - self.nb_x),
                self.step * (index_y - self.nb_y),
            ]
            for index_x in range(self.nb_x)
            for index_y in range(self.nb_y)
        )
        angle_radian = radians(self.angle)
        rotation_matrix = np.array(
            [
                [np.cos(angle_radian), -np.sin(angle_radian)],
                [np.sin(angle_radian), np.cos(angle_radian)],
            ]
        )
        return unrotate_theorical_position @ rotation_matrix
