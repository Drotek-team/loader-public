from dataclasses import dataclass
from typing import List, Tuple


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
