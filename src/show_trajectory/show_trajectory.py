from typing import List
import numpy as np
from dataclasses import dataclass

VELOCITY_ESTIMATION_INDEX = 1
ACCELERATION_ESTIMATION_INDEX = 2


@dataclass(frozen=True)
class TrajectoryInfo:
    position: np.ndarray
    velocity: np.ndarray = np.array(0)
    acceleration: np.ndarray = np.array(0)
    in_air: bool = False
    in_dance: bool = False


class DroneTrajectory:
    def __init__(self, drone_index: int, trajectory: List[TrajectoryInfo]):
        self.drone_index = drone_index
        self.trajectory = trajectory


class ShowTrajectory:
    def __init__(self, drones_trajectory: List[DroneTrajectory]):
        self.nb_drones = len(drones_trajectory)
        self.drones_trajectory = drones_trajectory
