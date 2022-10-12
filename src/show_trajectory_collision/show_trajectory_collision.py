from typing import List
import numpy as np
from dataclasses import dataclass

VELOCITY_ESTIMATION_INDEX = 1
ACCELERATION_ESTIMATION_INDEX = 2


@dataclass(frozen=True)
class TrajectoryCollisionInfo:
    position: np.ndarray
    in_air: bool = False


class DroneTrajectoryCollision:
    def __init__(self, drone_index: int, trajectory: List[TrajectoryCollisionInfo]):
        self.drone_index = drone_index
        self.trajectory = trajectory


class ShowTrajectoryCollision:
    def __init__(self, drones_trajectory_collision: List[DroneTrajectoryCollision]):
        self.nb_drones = len(drones_trajectory_collision)
        self.drones_trajectory_collision = drones_trajectory_collision
