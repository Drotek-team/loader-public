from typing import List
import numpy as np
from dataclasses import dataclass


@dataclass(frozen=True)
class TrajectoryCollisionInfo:
    frame: int
    position: np.ndarray
    in_air: bool


class DroneTrajectoryCollision:
    def __init__(self, drone_index: int, trajectory: List[TrajectoryCollisionInfo]):
        self.drone_index = drone_index
        self.trajectory = trajectory


class ShowTrajectoryCollision:
    def __init__(self, drones_trajectory_collision: List[DroneTrajectoryCollision]):
        self.nb_drones = len(drones_trajectory_collision)
        self.drones_trajectory_collision = drones_trajectory_collision

    @property
    def frames(self) -> List[int]:
        return [popo.frame for popo in self.drones_trajectory_collision[0].trajectory]
