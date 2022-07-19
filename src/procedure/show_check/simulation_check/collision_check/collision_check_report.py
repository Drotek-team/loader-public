from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class CollisionInfraction:
    first_drone_index: int
    second_drone_index: int
    in_air: bool
    collision_distance: float


class CollisionSliceCheckReport:
    def __init__(self, second: float):
        self.validation = False
        self.second = second
        self.collision_infractions: List[CollisionInfraction] = []

    def update(self) -> None:
        self.validation = len(self.collision_infractions) == 0


class CollisionCheckReport:
    def __init__(self):
        self.validation = False
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
