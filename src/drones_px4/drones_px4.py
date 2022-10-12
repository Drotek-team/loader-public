from typing import List


from .drone_px4.drone_px4 import DronePx4
from .drone_px4.events_size_easing import EventsSizeEasing, apply_dance_size_relief


class DronesPx4:
    def __init__(self, drones: List[DronePx4]):
        self.drones = drones

    def __iter__(self):
        for drone in self.drones:
            yield drone

    def __getitem__(self, drone_index: int):
        return self.drones[drone_index]

    def __len__(self):
        return len(self.drones)

    @property
    def nb_drone(self) -> int:
        return len(self.drones)

    def apply_dances_size_relief(self) -> None:
        events_size_easing = EventsSizeEasing()
        for drone in self.drones:
            apply_dance_size_relief(drone, events_size_easing)
