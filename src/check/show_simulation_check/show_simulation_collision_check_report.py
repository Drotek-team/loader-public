from dataclasses import dataclass
from typing import List

from ...report import Contenor, Displayer


@dataclass(frozen=True)
class CollisionInfraction(Displayer):
    first_drone_index: int
    second_drone_index: int
    in_air: bool
    collision_distance: float

    def get_report(self) -> str:
        status = "in air" if self.in_air else "on ground"
        return f"The drone {self.first_drone_index} and {self.second_drone_index} which are {status} are at a distance of {self.collision_distance}"


class CollisionSliceCheckReport(Contenor):
    def __init__(self, frame: int):
        self.name = f"Collision Slice {frame} check report"
        self.frame = frame
        self.collision_infractions: List[CollisionInfraction] = []

    def update(self) -> None:
        self.validation = len(self.collision_infractions) == 0


class ShowSimulationCollisionCheckReport(Contenor):
    def __init__(self, frames: List[int]):
        self.name = "Collision check report"
        self.collision_slices_check_report = [
            CollisionSliceCheckReport(frame) for frame in frames
        ]

    def update(self) -> None:
        self.validation = all(
            collision_slice_check_report.validation
            for collision_slice_check_report in self.collision_slices_check_report
        )
