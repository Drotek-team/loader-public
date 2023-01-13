from dataclasses import dataclass
from typing import List

import numpy as np


@dataclass(frozen=True)
class CollisionPositionInfo:
    frame: int
    position: np.ndarray
    in_air: bool

    def __eq__(self, other: "CollisionPositionInfo"):
        return (
            self.frame == other.frame
            and np.array_equal(self.position, other.position)
            and self.in_air == other.in_air
        )


class CollisionTrajectory:
    def __init__(self, drone_index: int, trajectory: List[CollisionPositionInfo]):
        self.drone_index = drone_index
        self._trajectory = trajectory

    @property
    def collision_position_infos(self) -> List[CollisionPositionInfo]:
        return self._trajectory


class CollisionShowTrajectory(List[CollisionTrajectory]):
    @property
    def frames(self) -> List[int]:
        return [
            collision_position_info.frame
            for collision_position_info in self[0].collision_position_infos
        ]

    @property
    def drone_number(self) -> int:
        return len(self)
