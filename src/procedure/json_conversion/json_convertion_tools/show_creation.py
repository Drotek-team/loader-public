import json
from dataclasses import dataclass
from typing import List, Tuple

from ....family_manager.family_manager import FamilyManager


@dataclass
class Dance:
    dance: List[int]


@dataclass
class Family:
    dances: List[Dance]
    x: int
    y: int
    z: int


@dataclass
class Show:
    def __init__(
        self,
        nb_x: int,
        nb_y: int,
        step: float,
        angle: int,
        hull: List[Tuple[float, float]],
        duration: int,
    ):
        self.families: List[Family] = []
        self.nb_x = nb_x
        self.nb_y = nb_y
        self.step = step
        self.angle = angle
        self.hull = hull
        self.duration = duration

    def update_families(
        self,
        first_positions: List[Tuple[int, int, int]],
        binaries: List[List[int]],
        family_manager: FamilyManager,
    ) -> None:
        dances = [Dance(binary) for binary in binaries]
        for family_index in range(
            (family_manager.nb_x * family_manager.nb_y)
            // family_manager.nb_drone_per_family,
        ):

            self.families.append(
                Family(
                    dances=dances[
                        family_index : family_index + family_manager.nb_drone_per_family
                    ],
                    x=first_positions[family_index][0],
                    y=first_positions[family_index][1],
                    z=first_positions[family_index][2],
                )
            )

    def get_json(self) -> str:
        class DummyClass:
            def __init__(self, show: Show):
                self.show = show

        return json.dumps(
            DummyClass(self), default=lambda o: o.__dict__, sort_keys=True, indent=4
        )
