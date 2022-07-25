import json
from dataclasses import dataclass
from typing import List, Tuple

from ....drones_manager.drones_manager import DroneExport
from ....family_manager.family_manager import FamilyManager


@dataclass(frozen=True)
class BinaryDance:
    bits: List[int] = []


class Family:
    def __init__(
        self, family_position: Tuple[int, int, int], binaries: List[BinaryDance]
    ):
        self.family_position = family_position
        self.binary_dances = binaries


class Show:
    def __init__(self) -> None:
        self.families: List[Family] = []
        self.convex_hull: List[Tuple[float, float]] = []
        self.nb_x: int = 0
        self.nb_y: int = 0
        self.step: float = 0
        self.angle: int = 0

    def update_families(
        self,
        drones: List[DroneExport],
        binaries: List[BinaryDance],
        family_manager: FamilyManager,
    ) -> None:
        drone_index = 0
        for drone_index in range(family_manager.nb_x * family_manager.nb_y - 1):
            self.families.append(
                Family(
                    drones[drone_index].first_xyz,
                    binaries[
                        drone_index
                        * family_manager.nb_drone_per_family : (drone_index + 1)
                        * family_manager.nb_drone_per_family
                    ],
                )
            )

    def update_parameter(
        self,
        nb_x: int,
        nb_y: int,
        step: float,
        angle: int,
        convex_hull: List[Tuple[float, float]],
    ):
        self.nb_x = nb_x
        self.nb_y = nb_y
        self.step = step
        self.angle = angle
        self.convex_hull = convex_hull

    def get_json(self) -> str:
        class DummyClass:
            def __init__(self, show: Show):
                self.show = show

        return json.dumps(
            DummyClass(self), default=lambda o: o.__dict__, sort_keys=True, indent=4
        )
