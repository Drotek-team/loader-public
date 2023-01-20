import math
from dataclasses import dataclass
from typing import List, Tuple

import numpy as np


# https://stackoverflow.com/questions/1878907/how-can-i-find-the-smallest-difference-between-two-angles-around-a-point
def angle_distance(first_angle_radian: float, second_angle_radian: float) -> float:
    first_angle, second_angle = math.degrees(first_angle_radian), math.degrees(
        second_angle_radian
    )
    return abs((second_angle - first_angle + 180) % 360 - 180)


# TODO: there is a logic duplication here, not very pretty...
# Very ugly to be honest
@dataclass()
class ShowConfiguration:
    nb_x: int  # Number of families on the x-axis (west/east) during the takeoff
    nb_y: int  # Number of families on the y-axis (south/north) during the takeoff
    nb_drone_per_family: int  # Number of drones in each families
    step: float  # Distance separating the families during the takeoff in meter
    angle_takeoff: float  # Angle of the takeoff grid in radian
    duration: float  # Duration of the show in second
    hull: List[
        Tuple[float, float]
    ]  # List of the relative coordinate (ENU and meter) symbolysing a convex hull of a show
    altitude_range: Tuple[
        float, float
    ]  # Relative coordinate (ENU and meter) symbolising the range of the z-axis

    # TODO: See the documentation here
    @staticmethod
    def _is_grid_angle_fuzzy(nb_x: int, nb_y: int) -> bool:
        return nb_x == 1 and nb_y != 1

    def __post_init__(self):
        if self.nb_x == 1 and self.nb_y == 1:
            self.step = 0.0
            self.angle_takeoff = 0.0
        if self._is_grid_angle_fuzzy(self.nb_x, self.nb_y):
            self.nb_y, self.nb_x = self.nb_x, self.nb_y
            self.angle_takeoff += 0.5 * np.pi

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, ShowConfiguration):
            return False
        return (
            self.nb_x == __o.nb_x
            and self.nb_y == __o.nb_y
            and self.nb_drone_per_family == __o.nb_drone_per_family
            and np.abs(self.step - __o.step) < 1e-6
            and angle_distance(self.angle_takeoff, __o.angle_takeoff) < 1e-6
            and self.duration == __o.duration
            and self.hull == __o.hull
            and self.altitude_range == __o.altitude_range
        )
