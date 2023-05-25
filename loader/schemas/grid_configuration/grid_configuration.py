from dataclasses import dataclass

import numpy as np


# https://stackoverflow.com/questions/1878907/how-can-i-find-the-smallest-difference-between-two-angles-around-a-point
def is_angles_equal(first_angle_radian: float, second_angle_radian: float) -> bool:
    first_angle, second_angle = np.degrees(first_angle_radian), np.degrees(second_angle_radian)
    return abs((second_angle - first_angle + 180) % 360 - 180) < 1e-6


@dataclass()
class GridConfiguration:
    nb_x: int = 1  # Number of families on the x-axis (west/east) during the takeoff
    nb_y: int = 1  # Number of families on the y-axis (south/north) during the takeoff
    nb_drone_per_family: int = 1  # Number of drones in each families
    step: float = 1.5  # Distance separating the families during the takeoff in meter
    angle_takeoff: float = 0.0  # Angle of the takeoff grid in radian
