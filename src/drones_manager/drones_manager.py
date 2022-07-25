from typing import List, Tuple

import numpy as np

from ..parameter.parameter import JsonConvertionConstant
from .convex_hull import calculate_convex_hull
from .drone.drone import DroneExport
from .drone.events.position_events import PositionEvent
from .drone.events_size_easing import EventsSizeEasing, apply_dance_size_relief
from .trajectory_simulation_manager.trajectory_simulation_manager import (
    TrajectorySimulationManager,
)


class DronesManager:
    def __init__(self, drones: List[DroneExport]):
        self.drones = drones

    @property
    def nb_drone(self) -> int:
        return len(self.drones)

    @property
    def last_position_events(self) -> List[PositionEvent]:
        return [drone.last_position_event for drone in self.drones]

    @property
    def duration(self) -> int:
        return max(drone.last_position_event.timecode for drone in self.drones)

    @property
    def first_horizontal_positions(self) -> List[Tuple]:
        return [
            drone.position_events.get_values_by_event_index(0)[0:2]
            for drone in self.drones
        ]

    def get_trajectory_simulation_manager(
        self, json_convertion_constant: JsonConvertionConstant
    ) -> TrajectorySimulationManager:
        trajectory_simulation_manager = TrajectorySimulationManager(len(self.drones))
        for trajectory_simulation, drone in zip(
            trajectory_simulation_manager.trajectories_simulation, self.drones
        ):
            trajectory_simulation.initialize_position_simulation(
                drone.position_events.event_list, json_convertion_constant
            )
        return trajectory_simulation_manager

    @property
    def convex_hull(self) -> List[np.ndarray]:
        return calculate_convex_hull(list(np.array(self.first_horizontal_positions)))

    def apply_dances_size_relief(self) -> None:
        events_size_easing = EventsSizeEasing()
        for drone in self.drones:
            apply_dance_size_relief(drone, events_size_easing)
