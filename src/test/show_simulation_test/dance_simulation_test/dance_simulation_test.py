from typing import List

import numpy as np
import pytest
from src.drones_manager.drone.events.position_events import PositionEvent

from ....drones_manager.drones_manager import Drone, DronesManager
from ....parameter.parameter import Parameter
from ....show_simulation.dance_simulation.position_simulation import (
    linear_interpolation,
)
from ....show_simulation.show_simulation import ShowSimulation


def get_show_simulation(position_events: List[PositionEvent]) -> ShowSimulation:
    parameter = Parameter()
    parameter.load_parameter()
    show_simulation = ShowSimulation(
        nb_drones=1,
    )
    drone = Drone(0)
    drone.add_position(0, (0, 0, 0))
    drone.add_position(
        parameter.takeoff_parameter.takeoff_duration,
        (0, 0, parameter.takeoff_parameter.takeoff_altitude),
    )
    for position_event in position_events:
        position = position_event.get_values()
        drone.add_position(
            parameter.takeoff_parameter.takeoff_duration + position_event.timecode,
            (
                position[0],
                position[1],
                position[2] - parameter.takeoff_parameter.takeoff_altitude,
            ),
        )
    drones_manager = DronesManager([drone])
    show_simulation.update_show_slices(
        drones_manager.last_position_events,
        parameter.timecode_parameter,
        parameter.land_parameter,
    )
    show_simulation.add_dance_simulation(
        drone,
        parameter.timecode_parameter,
        parameter.takeoff_parameter,
        parameter.land_parameter,
        parameter.json_convertion_constant,
    )
    show_simulation.update_slices_implicit_values(
        parameter.timecode_parameter,
        parameter.json_convertion_constant,
    )
    return show_simulation


def test_valid_show_flags():
    parameter = Parameter()
    parameter.load_parameter()
    position_event_1 = PositionEvent(250, 0, 0, 0)
    position_event_2 = PositionEvent(500, 0, 0, 0)
    position_event_3 = PositionEvent(750, 0, 0, 0)
    valid_show_simulation = get_show_simulation(
        [position_event_1, position_event_2, position_event_3]
    )
    slice_takeoff_end_index = (
        parameter.takeoff_parameter.takeoff_duration
        // parameter.timecode_parameter.position_timecode_rate
    )
    slice_land_begin_index = slice_takeoff_end_index + 3
    slice_land_end_index = slice_land_begin_index + (
        parameter.land_parameter.get_land_timecode_delta(
            parameter.takeoff_parameter.takeoff_altitude
        )
        // parameter.timecode_parameter.position_timecode_rate
    )
    assert len(valid_show_simulation.show_slices) == slice_land_end_index + 1
    assert all(
        show_slice.in_air_flags[0]
        for show_slice in valid_show_simulation.show_slices[:slice_takeoff_end_index]
    )
    assert all(
        not (show_slice.in_dance_flags[0])
        for show_slice in valid_show_simulation.show_slices[:slice_takeoff_end_index]
    )
    assert all(
        show_slice.in_air_flags[0]
        for show_slice in valid_show_simulation.show_slices[
            slice_takeoff_end_index:slice_land_begin_index
        ]
    )
    assert all(
        show_slice.in_dance_flags[0]
        for show_slice in valid_show_simulation.show_slices[
            slice_takeoff_end_index:slice_land_begin_index
        ]
    )
    assert all(
        show_slice.in_air_flags[0]
        for show_slice in valid_show_simulation.show_slices[
            slice_land_begin_index:slice_land_end_index
        ]
    )
    assert all(
        not (show_slice.in_dance_flags[0])
        for show_slice in valid_show_simulation.show_slices[
            slice_land_begin_index:slice_land_end_index
        ]
    )
    assert not (valid_show_simulation.show_slices[-1].in_air_flags[0])
    assert not (valid_show_simulation.show_slices[-1].in_dance_flags[0])
