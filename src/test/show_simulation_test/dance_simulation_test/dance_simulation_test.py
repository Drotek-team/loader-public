import os
from typing import List

from ....drones_manager.drone.events.position_events import PositionEvent
from ....drones_manager.drones_manager import DroneExport, DronesManager
from ....parameter.parameter import Parameter
from ....show_simulation.show_simulation import ShowSimulation, get_slices


def get_show_simulation(position_events: List[PositionEvent]) -> ShowSimulation:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    drone = DroneExport(0)
    drone.add_position(0, (0, 0, 0))
    drone.add_position(
        parameter.frame_parameter.json_fps
        * parameter.takeoff_parameter.takeoff_duration_second,
        (
            0,
            0,
            -parameter.json_convertion_constant.METER_TO_CENTIMETER_RATIO
            * parameter.takeoff_parameter.takeoff_altitude_meter,
        ),
    )
    for position_event in position_events:
        position = position_event.get_values()
        drone.add_position(
            parameter.frame_parameter.json_fps
            * parameter.takeoff_parameter.takeoff_duration_second
            + position_event.frame,
            (
                position[0],
                position[1],
                -parameter.json_convertion_constant.METER_TO_CENTIMETER_RATIO
                * parameter.takeoff_parameter.takeoff_altitude_meter
                + position[2],
            ),
        )

    drones_manager = DronesManager([drone])
    show_simulation = ShowSimulation(
        get_slices(
            drones_manager.get_trajectory_simulation_manager(
                parameter.json_convertion_constant
            ),
            parameter.frame_parameter,
            parameter.takeoff_parameter,
            parameter.land_parameter,
        )
    )
    return show_simulation


def test_valid_show_flags():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    position_event_1 = PositionEvent(6, 0, 0, 0)
    position_event_2 = PositionEvent(12, 0, 0, 0)
    position_event_3 = PositionEvent(18, 0, 0, 0)
    valid_show_simulation = get_show_simulation(
        [position_event_1, position_event_2, position_event_3]
    )
    slice_takeoff_end_index = int(
        parameter.takeoff_parameter.takeoff_duration_second
        * parameter.frame_parameter.position_fps
    )
    slice_land_begin_index = slice_takeoff_end_index + 3
    slice_land_end_index = slice_land_begin_index + int(
        (
            parameter.land_parameter.get_land_second_delta(
                parameter.takeoff_parameter.takeoff_altitude_meter
            )
            * parameter.frame_parameter.position_fps
        )
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
