from dataclasses import dataclass
from typing import List
import numpy as np


class TrajectorySimulation:
    def __init__(
        self,
        drone_positions: List[np.ndarray],
        drone_in_air: List[bool],
        drone_in_dance: List[bool],
    ):
        self.drone_positions = drone_positions
        self.drone_in_air = drone_in_air
        self.drone_in_dance = drone_in_dance

    def concatenate_trajectory(
        self, trajectory_simulation: "TrajectorySimulation"
    ) -> None:
        self.drone_positions += trajectory_simulation.drone_positions
        self.drone_in_air += trajectory_simulation.drone_in_air
        self.drone_in_dance += trajectory_simulation.drone_in_dance
