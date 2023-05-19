from dataclasses import dataclass

import numpy as np


@dataclass()
class GridConfiguration:
    nb_x: int = 1  # Number of families on the x-axis (west/east) during the takeoff
    nb_y: int = 1  # Number of families on the y-axis (south/north) during the takeoff
    nb_drone_per_family: int = 1  # Number of drones in each families
    step: float = 1.5  # Distance separating the families during the takeoff in meter
    angle_takeoff: float = 0.0  # Angle of the takeoff grid in radian

    @staticmethod
    def _is_grid_one_family(nb_x: int, nb_y: int) -> bool:
        return nb_x == 1 and nb_y == 1

    @staticmethod
    def _is_grid_angle_fuzzy(nb_x: int, nb_y: int) -> bool:
        return nb_x == 1 and nb_y != 1

    def __post_init__(self) -> None:
        if self._is_grid_one_family(self.nb_x, self.nb_y):
            self.step = 0.0
            self.angle_takeoff = 0.0
        if self._is_grid_angle_fuzzy(self.nb_x, self.nb_y):
            self.nb_y, self.nb_x = self.nb_x, self.nb_y
            self.angle_takeoff += 0.5 * np.pi
