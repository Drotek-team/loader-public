from dataclasses import dataclass
from typing import List

from ...report import *


@dataclass(frozen=True)
class CollisionInfraction(ErrorMessage):
    name: str
    drone_index_1: int
    drone_index_2: int
    distance: float
    in_air: bool

    @property
    def user_validation(self) -> bool:
        return False

    def display_message(self, indentation_level: int, indentation_type: str) -> str:
        return (
            f"{indentation_level*indentation_type}Collision between drone {self.drone_index_1} and drone {self.drone_index_2} "
            f"{'in air' if self.in_air else 'on ground'} with a distance of {self.distance}"
        )


class ShowSimulationCollisionCheckReport(Contenor):
    def __init__(self):
        self.name = "Collision check report"
        self.collision_slices_check_report: List[ErrorMessageList] = []

    def add_slice_report(
        self, frame: int, collision_infractions: List[CollisionInfraction]
    ) -> None:
        self.collision_slices_check_report.append(
            ErrorMessageList(f"Frame {frame}", collision_infractions)  # type: ignore[Have fun cleaning this]
        )
