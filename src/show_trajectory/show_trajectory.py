from typing import List
import numpy as np

### TO DO: these names are kind of shitty
VELOCITY_ESTIMATION_INDEX = 1
ACCELERATION_ESTIMATION_INDEX = 2


class DroneTrajectory:
    ### TO DO: Make a data class for that,  no ?
    ### As the object is kind of risky, the migration should be bullet proof
    def __init__(
        self,
        drone_positions: List[np.ndarray],
        drone_in_air: List[bool],
        drone_in_dance: List[bool],
    ):
        self.drone_positions = drone_positions
        self.drone_velocities: List[np.ndarray] = []
        self.drone_accelerations: List[np.ndarray] = []
        self.drone_in_air = drone_in_air
        self.drone_in_dance = drone_in_dance

    def concatenate_trajectory(self, drone_trajectory: "DroneTrajectory") -> None:
        self.drone_positions += drone_trajectory.drone_positions
        self.drone_in_air += drone_trajectory.drone_in_air
        self.drone_in_dance += drone_trajectory.drone_in_dance

    def update_implicit_performance(self, position_frame_frequence: int) -> None:
        for trajectory_index in range(
            ACCELERATION_ESTIMATION_INDEX, len(self.drone_positions)
        ):
            self.drone_velocities[trajectory_index] = position_frame_frequence * (
                self.drone_positions[trajectory_index]
                - self.drone_positions[trajectory_index - VELOCITY_ESTIMATION_INDEX]
            )
            self.drone_accelerations[trajectory_index] = position_frame_frequence * (
                self.drone_velocities[trajectory_index]
                - self.drone_velocities[trajectory_index - VELOCITY_ESTIMATION_INDEX]
            )


class ShowTrajectory:
    def __init__(self, drones_trajectory: List[DroneTrajectory]):
        self.drones_trajectory = drones_trajectory

    # @property
    # def frames(self) -> List[int]:
    #     return self.drones_trajectory[0].drone_frames

    @property
    def nb_drones(self) -> int:
        return len(self.drones_trajectory)
