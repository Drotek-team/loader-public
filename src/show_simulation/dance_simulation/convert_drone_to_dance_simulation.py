import numpy as np

from ...drones_manager.drone.drone import Drone
from ...parameter.parameter import (
    JsonConvertionConstant,
    LandParameter,
    TakeoffParameter,
    TimecodeParameter,
)
from .dance_simulation import DanceSimulation
from .flight_simulation import flight_simulation
from .land_simulation import land_simulation
from .stand_by_simulation import stand_by_simulation
from .takeoff_simulation import takeoff_simulation


def convert_drone_to_dance_simulation(
    drone: Drone,
    last_timecode: int,
    timecode_parameter: TimecodeParameter,
    takeoff_parameter: TakeoffParameter,
    land_parameter: LandParameter,
    json_convertion_constant: JsonConvertionConstant,
) -> DanceSimulation:
    dance_simulation = DanceSimulation()
    position_events = drone.position_events
    if position_events.nb_events == 1:
        dance_simulation.update(
            stand_by_simulation(
                timecode_parameter.show_timecode_begin,
                position_events.get_values_by_event_index(0),
                timecode_parameter,
                json_convertion_constant,
            )
        )
        return dance_simulation
    dance_simulation.update(
        stand_by_simulation(
            timecode_parameter.show_timecode_begin,
            position_events.get_timecode_by_event_index(0),
            position_events.get_values_by_event_index(0),
            timecode_parameter,
            json_convertion_constant,
        )
    )
    dance_simulation.update(
        takeoff_simulation(
            position_events.get_values_by_event_index(0),
            timecode_parameter,
            takeoff_parameter,
            json_convertion_constant,
        )
    )
    dance_simulation.update(
        flight_simulation(
            position_events.event_list[1:],
            timecode_parameter,
            json_convertion_constant,
        )
    )
    dance_simulation.update(
        land_simulation(
            position_events.get_values_by_event_index(-1),
            timecode_parameter,
            land_parameter,
            json_convertion_constant,
        )
    )
    last_position = position_events.get_values_by_event_index(-1)
    dance_simulation.update(
        stand_by_simulation(
            position_events.get_timecode_by_event_index(-1),
            last_timecode + timecode_parameter.position_timecode_rate,
            (last_position[0], last_position[1], 0),
            timecode_parameter,
            json_convertion_constant,
        )
    )
    return dance_simulation
