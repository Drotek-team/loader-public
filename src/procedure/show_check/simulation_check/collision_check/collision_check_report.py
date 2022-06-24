from typing import List


class DroneCollisionCheckReport:
    def __init__(self):
        self.validation = False


class CollisionCheckReport:
    def __init__(self, nb_drone: int):
        self.validation = False
        self.drones_collision_check_report = [
            DroneCollisionCheckReport() for _ in range(nb_drone)
        ]

    def update(
        self,
        endangered_drone_on_ground_indices: List[int],
        endangered_drone_in_air_flags: List[int],
    ) -> None:
        for endangered_drone_on_ground_index in endangered_drone_on_ground_indices:
            self.drones_collision_check_report[endangered_drone_on_ground_index].update(
                False, "on_ground"
            )
        for endangered_drone_in_air_index in endangered_drone_in_air_flags:
            self.drones_collision_check_report[endangered_drone_in_air_index].update(
                False, "in_air"
            )
        self.validation = all(
            drone_collision_check_report.validation
            for drone_collision_check_report in self.drones_collision_check_report
        )
