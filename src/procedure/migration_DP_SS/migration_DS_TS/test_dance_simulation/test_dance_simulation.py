import os
from typing import List

from .....drones_px4.drone_px4.events.position_events import PositionEvent
from .....drones_px4.drones_px4 import DronePx4, DronesPx4
from .....parameter.parameter import Parameter
from .....show_simulation.show_simulation import ShowSimulation
from ...DP_to_SS_procedure import DP_to_SS_procedure
from ....migration_DP_DU.data_convertion_format import XyzConvertionStandard


def get_show_simulation(position_events: List[PositionEvent]) -> ShowSimulation:
    parameter = Parameter()
    xyz_convertion_standard = XyzConvertionStandard()
    parameter.load_parameter(os.getcwd())
    drone = DronePx4(0)
    drone.add_position(0, (0, 0, 0))
    drone.add_position(
        int(
            parameter.frame_parameter.json_fps
            * parameter.takeoff_parameter.takeoff_duration_second
        ),
        xyz_convertion_standard.from_user_xyz_to_px4_xyz(
            (
                0,
                0,
                parameter.takeoff_parameter.takeoff_altitude_meter,
            )
        ),
    )
    for position_event in position_events:
        position = position_event.xyz
        drone.add_position(
            int(
                parameter.frame_parameter.json_fps
                * parameter.takeoff_parameter.takeoff_duration_second
            )
            + position_event.frame,
            xyz_convertion_standard.from_user_xyz_to_px4_xyz(
                (
                    position[0],
                    position[1],
                    parameter.takeoff_parameter.takeoff_altitude_meter,
                )
            ),
        )

    drones_px4 = DronesPx4([drone])
    show_simulation = DP_to_SS_procedure(
        drones_px4,
        parameter.frame_parameter,
        parameter.takeoff_parameter,
        parameter.land_parameter,
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
