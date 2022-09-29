from typing import List, Tuple


from .convex_hull import calculate_convex_hull
from .drone_px4.drone_px4 import DronePx4
from .drone_px4.events.position_events import PositionEvent
from .drone_px4.events_size_easing import EventsSizeEasing, apply_dance_size_relief


class DronesPx4:
    def __init__(self, drones: List[DronePx4]):
        self.drones = drones

    @property
    def nb_drone(self) -> int:
        return len(self.drones)

    @property
    def last_position_events(self) -> List[PositionEvent]:
        return [drone.last_position_event for drone in self.drones]

    @property
    def duration(self) -> int:
        return max(drone.last_position_event.frame for drone in self.drones)

    @property
    def first_horizontal_positions(self) -> List[Tuple[int, int]]:
        return [
            drone.position_events.get_values_by_event_index(0)[0:2]
            for drone in self.drones
        ]

    @property
    def convex_hull(self) -> List[Tuple[int, int]]:
        return calculate_convex_hull(self.first_horizontal_positions)

    @property
    def altitude_range(self) -> Tuple[int, int]:
        z_positions = [
            position_event.get_values()[2]
            for drone in self.drones
            for position_event in drone.position_events.event_list
        ]
        return (min(z_positions), max(z_positions))

    def apply_dances_size_relief(self) -> None:
        events_size_easing = EventsSizeEasing()
        for drone in self.drones:
            apply_dance_size_relief(drone, events_size_easing)
