from typing import List

from loader.report.simulation.position_simulation import SimulationInfo


class CollisionTrajectory:
    def __init__(self, drone_index: int, trajectory: List[SimulationInfo]) -> None:
        self.drone_index = drone_index
        self._trajectory = trajectory

    @property
    def collision_position_infos(self) -> List[SimulationInfo]:
        return self._trajectory


class ShowCollisionTrajectory(List[CollisionTrajectory]):
    @property
    def frames(self) -> List[int]:
        return list(
            range(
                min(
                    collision_trajectory.collision_position_infos[0].frame
                    for collision_trajectory in self
                ),
                max(
                    collision_trajectory.collision_position_infos[-1].frame
                    for collision_trajectory in self
                )
                + 1,
            ),
        )
