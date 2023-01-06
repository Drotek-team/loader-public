from typing import List

from ...report import *

# class CollisionInfraction(Displayer):
#     first_drone_index: int
#     second_drone_index: int
#     in_air: bool
#     collision_distance: float

#     def get_report(self) -> str:
#         status = "in air" if self.in_air else "on ground"
#         return f"The drone {self.first_drone_index} and {self.second_drone_index} which are {status} are at a distance of {self.collision_distance}"


class ContenorSliceCheckReport(Contenor):
    def __init__(self, name: str):
        self.name = name
        self.collision_infractions: List[Displayer] = []


class ShowSimulationCollisionCheckReport(Contenor):
    def __init__(self, frames: List[int]):
        self.name = "Collision check report"
        self.collision_slices_check_report = [
            ContenorSliceCheckReport(f"Collision Slice check report {frame}")
            for frame in frames
        ]

    def update(self) -> None:
        self.validation = all(
            collision_slice_check_report.validation
            for collision_slice_check_report in self.collision_slices_check_report
        )
