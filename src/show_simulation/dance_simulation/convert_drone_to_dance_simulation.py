import numpy as np

from ...drones_manager.drone.drone import Drone
from ...parameter.parameter import LandParameter, TakeoffParameter, TimecodeParameter
from .dance_simulation import DanceSimulation
from .flight_simulation import flight_simulation
from .land_simulation import land_simulation
from .stand_by_simulation import stand_by_simulation
from .takeoff_simulation import takeoff_simulation


def convert_drone_to_dance_simulation(
    drone: Drone,
    timecode_show_end: int,
    timecode_parameter: TimecodeParameter,
    takeoff_parameter: TakeoffParameter,
    land_parameter: LandParameter,
) -> DanceSimulation:
    position_events = drone.position_events
    dance_simulation = DanceSimulation()
    if len(position_events) == 1:
        dance_simulation.update(
            stand_by_simulation(
                timecode_parameter.show_timecode_begin,
                timecode_show_end,
                position_events.get_values_by_event_index(0),
                timecode_parameter,
            )
        )
        return dance_simulation
    dance_simulation.update(
        stand_by_simulation(
            timecode_parameter.show_timecode_begin,
            position_events.get_timecode_by_event_index(0),
            position_events.get_values_by_event_index(0),
            timecode_parameter,
        )
    )
    dance_simulation.update(
        takeoff_simulation(
            position_events.get_timecode_by_event_index(0),
            position_events.get_timecode_by_event_index(1),
            position_events.get_values_by_event_index(0),
            position_events.get_values_by_event_index(1),
            timecode_parameter,
            takeoff_parameter,
        )
    )
    dance_simulation.update(
        flight_simulation(
            {
                position_events.get_timecode_by_event_index(
                    event_index
                ): position_events.get_values_by_event_index(event_index)
                for event_index in range(1, len(position_events))
            },
            timecode_parameter,
        )
    )
    dance_simulation.update(
        land_simulation(
            position_events.get_timecode_by_event_index(-1),
            position_events.get_values_by_event_index(-1),
            timecode_parameter,
            land_parameter,
        )
    )
    last_position = position_events.get_values_by_event_index(-1)
    dance_simulation.update(
        stand_by_simulation(
            len(dance_simulation) * timecode_parameter.position_timecode_rate,
            timecode_show_end,
            (last_position[0], last_position[1], 0),
            timecode_parameter,
        )
    )
    return dance_simulation
