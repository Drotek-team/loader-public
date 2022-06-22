from dataclasses import dataclass
from typing import List, Tuple

import numpy as np

from ...drones_manager.drone.drone import Drone
from ...parameter.parameter import TimecodeParameter
from .flight_simulation import flight_simulation
from .land_simulation import land_simulation
from .stand_by_simulation import stand_by_simulation
from .takeoff_simulation import takeoff_simulation


@dataclass(frozen=True)
class DroneSimulationConvertor:
    CENTIMETER_TO_METER_RATIO: float = 1e-2
    TIMECODE_TO_SECOND_RATIO: float = 1e-3

    def event_xyz_to_numpy_position(
        self, xyz: Tuple[float, float, float]
    ) -> np.ndarray:
        return np.array(
            (
                self.CENTIMETER_TO_METER_RATIO * xyz[1],
                self.CENTIMETER_TO_METER_RATIO * xyz[0],
                -self.CENTIMETER_TO_METER_RATIO * xyz[2],
            )
        )


class DanceSimulation:
    def __init__(self):
        self.drone_positions: List[np.ndarray] = []
        self.drone_in_air: List[bool] = []
        self.drone_in_dance: List[bool] = []

    def update(
        self, new_values: Tuple[List[np.ndarray], List[bool], List[bool]]
    ) -> None:
        self.drone_positions += new_values[0]
        self.drone_in_air += new_values[1]
        self.drone_in_dance += new_values[2]

    @property
    def numpy_values(self) -> Tuple[List[np.ndarray], List[bool], List[bool]]:
        return (self.drone_positions, self.drone_in_air, self.drone_in_dance)


def convert_drone_to_dance_simulation(
    drone: Drone,
    show_end_timecode: int,
    timecode_parameter: TimecodeParameter,
) -> DanceSimulation:
    position_events = drone.position_events
    dance_simulation = DanceSimulation()
    dance_simulation.update(
        stand_by_simulation(
            position_events.get_timecode_by_event_index(0),
            np.array(position_events.get_values_by_event_index(0)),
            timecode_parameter,
        )
    )
    dance_simulation.update(
        takeoff_simulation(
            position_events.get_timecode_by_event_index(0),
            position_events.get_timecode_by_event_index(1),
            np.array(position_events.get_values_by_event_index(0)),
            np.array(position_events.get_values_by_event_index(1)),
        )
    )
    dance_simulation.update(
        flight_simulation(
            {
                position_events.get_timecode_by_event_index(event_index): np.array(
                    position_events.get_values_by_event_index(event_index)
                )
                for event_index in range(1, len(position_events))
            },
            timecode_parameter,
        )
    )
    dance_simulation.update(
        land_simulation(
            position_events.get_timecode_by_event_index(-1),
            position_events.get_values_by_event_index(-1),
            show_end_timecode,
            timecode_parameter,
        )
    )
    return dance_simulation
