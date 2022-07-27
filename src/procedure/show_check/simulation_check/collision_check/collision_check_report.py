from dataclasses import dataclass
from typing import List

from ....report import Contenor, Displayer


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
    def __init__(self, second: float):
        self.name = f"Collsion Slice {second} check report"
        self.second = second
        self.collision_infractions: List[CollisionInfraction] = []

    def update(self) -> None:
        self.validation = len(self.collision_infractions) == 0


class CollisionCheckReport(Contenor):
    def __init__(self):
        self.name = "Collision check report"
        self.collision_slices_check_report: List[CollisionSliceCheckReport] = []

    def initialize_collision_slice_check_report(self, seconds: List[float]) -> None:
        self.collision_slices_check_report = [
            CollisionSliceCheckReport(second) for second in seconds
        ]

    def update(self) -> None:
        self.validation = all(
            collision_slice_check_report.validation
            for collision_slice_check_report in self.collision_slices_check_report
        )
