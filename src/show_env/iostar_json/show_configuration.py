from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
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
