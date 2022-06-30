import json
from dataclasses import dataclass
from typing import List, Tuple

from ..drones_manager.drone.drone_encoder import DroneEncoder
from ..drones_manager.drones_manager import Drone
from ..family_manager.family_manager import FamilyManager
from ..procedure.json_creation.json_creation_report import JsonCreationReport


@dataclass(frozen=True)
class BinaryDance:
    bits: List[int] = []


class Family:
    def __init__(self):
        self.family_position: Tuple[int, int, int] = (0, 0, 0)
        self.dance: List[BinaryDance] = []

    def update_position(self, position: Tuple[int, int, int]) -> None:
        self.family_position = position

    def update_dances(self, drones: List[Drone], drone_encoder: DroneEncoder) -> None:
        for drone in drones:
            self.dance.append(drone_encoder.encode(drone))


class Show:
    def __init__(self) -> None:
        self.families: List[List[Family]] = []
        self.convex_hull: List[Tuple[float, float]] = []
        self.nb_x: int = 0
        self.nb_y: int = 0
        self.step: float = 0
        self.angle: int = 0

    def update_families(
        self,
        drones: List[Drone],
        family_manager: FamilyManager,
        json_creation_report: JsonCreationReport,
    ) -> None:
        drone_index = 0
        drone_encoder = DroneEncoder()
        for drone_index in range(family_manager.nb_x * family_manager.nb_y - 1):
            family = Family()
            family.update_position(drones[drone_index].first_xyz)
            family.update_dances(
                drones[
                    drone_index
                    * family_manager.nb_drone_per_family : (drone_index + 1)
                    * family_manager.nb_drone_per_family
                ],
                drone_encoder,
            )

    def update_parameter(
        self,
        nb_x: int,
        nb_y: int,
        step: float,
        angle: int,
        convex_hull: List[Tuple[float, float]],
        json_creation_report: JsonCreationReport,
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
