from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class DroneCollisionInfraction:
    timecode: int
    other_drone_index: int
    in_air: bool
    collision_distance: float


@dataclass(frozen=True)
class CollisionInfraction:
    timecode: int
    first_drone_index: int
    second_drone_index: int
    in_air: bool
    collision_distance: float


class DroneCollisionCheckReport:
    def __init__(self, drone_index):
        self.validation = False
        self.drone_index = drone_index
        self.drone_collisions_infraction: List[DroneCollisionInfraction] = []

    def update(self) -> None:
        self.validation = len(self.drone_collisions_infraction) == 0

    def add_drone_collision_infraction(
        self,
        timecode: int,
        other_drone_index: int,
        in_air: bool,
        collision_distance: float,
    ) -> None:
        self.drone_collisions_infraction.append(
            DroneCollisionInfraction(
                timecode, other_drone_index, in_air, collision_distance
            )
        )


class CollisionCheckReport:
    def __init__(self, nb_drones: int):
        self.validation = False
        self.drones_collision_check_report = [
            DroneCollisionCheckReport(drone_index) for drone_index in range(nb_drones)
        ]

    def update(self) -> None:
        self.validation = all(
            drones_collision_check_report.validation
            for drones_collision_check_report in self.drones_collision_check_report
        )

    def update_drones_collision_check_report(
        self, collision_infractions: List[CollisionInfraction]
    ) -> None:
        for collision_infraction in collision_infractions:
            self.drones_collision_check_report[
                collision_infraction.first_drone_index
            ].add_drone_collision_infraction(
                collision_infraction.timecode,
                collision_infraction.second_drone_index,
                collision_infraction.in_air,
                collision_infraction.collision_distance,
            )
