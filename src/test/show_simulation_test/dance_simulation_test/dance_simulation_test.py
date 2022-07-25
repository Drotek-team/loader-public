import os
from typing import List

from ....drones_manager.drone.events.position_events import PositionEvent
from ....drones_manager.drones_manager import Drone, DronesManager
from ....parameter.parameter import Parameter
from ....show_simulation.show_simulation import ShowSimulation


def get_show_simulation(position_events: List[PositionEvent]) -> ShowSimulation:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    drone = Drone(0)
    drone.add_position(0, (0, 0, 0))
    drone.add_position(
        parameter.takeoff_parameter.takeoff_duration,
        (0, 0, -parameter.takeoff_parameter.takeoff_altitude),
    )
    for position_event in position_events:
        position = position_event.get_values()
        drone.add_position(
            parameter.takeoff_parameter.takeoff_duration + position_event.timecode,
            (
                position[0],
                position[1],
                -parameter.takeoff_parameter.takeoff_altitude + position[2],
            ),
        )

    drones_manager = DronesManager([drone])
    trajectory_simulation_manager = drones_manager.get_trajectory_simulation_manager(
        parameter.json_convertion_constant
    )
    show_simulation = ShowSimulation(
        len(trajectory_simulation_manager.trajectories_simulation),
        trajectory_simulation_manager.get_last_second(parameter.land_parameter),
    )
    show_simulation.update_show_slices(
        parameter.timecode_parameter,
    )
    for trajectory_simulation in trajectory_simulation_manager.trajectories_simulation:
        show_simulation.add_dance_simulation(
            trajectory_simulation,
            parameter.timecode_parameter,
            parameter.takeoff_parameter,
            parameter.land_parameter,
        )
    return show_simulation


def test_valid_show_flags():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    position_event_1 = PositionEvent(250, 0, 0, 0)
    position_event_2 = PositionEvent(500, 0, 0, 0)
    position_event_3 = PositionEvent(750, 0, 0, 0)
    valid_show_simulation = get_show_simulation(
        [position_event_1, position_event_2, position_event_3]
    )
    slice_takeoff_end_index = int(
        parameter.takeoff_parameter.takeoff_simulation_duration
        / parameter.timecode_parameter.position_second_rate
    )
    slice_land_begin_index = slice_takeoff_end_index + 3
    slice_land_end_index = slice_land_begin_index + int(
        (
            parameter.land_parameter.get_land_second_delta(
                parameter.takeoff_parameter.takeoff_simulation_altitude
            )
            / parameter.timecode_parameter.position_second_rate
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
