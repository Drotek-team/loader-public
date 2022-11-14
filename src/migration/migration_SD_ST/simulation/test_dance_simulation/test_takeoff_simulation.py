import os
from typing import Tuple

import pytest

from src.migration.migration_SD_ST.simulation.position_simulation import SimulationInfo

from .....parameter.parameter import Parameter
from .....show_dev.show_dev import PositionEventDev
from ...simulation.takeoff_simulation import takeoff_simulation
from ..in_air_flight_simulation import linear_interpolation


@pytest.fixture
def valid_position_events_dev() -> Tuple[PositionEventDev, PositionEventDev]:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    FRAME_START = 0
    POSITION = (0.0, 0.0, 0.0)
    return PositionEventDev(FRAME_START, POSITION), PositionEventDev(
        FRAME_START
        + int(
            parameter.frame_parameter.json_fps
            * parameter.takeoff_parameter.takeoff_duration_second
        ),
        (
            POSITION[0],
            POSITION[1],
            POSITION[2] + parameter.takeoff_parameter.takeoff_altitude_meter,
        ),
    )


def test_takeoff_simulation(
    valid_position_events_dev: Tuple[PositionEventDev, PositionEventDev]
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())

    first_position_event, second_position_event = (
        valid_position_events_dev[0],
        valid_position_events_dev[1],
    )
    real_takeoff_simulation_infos = takeoff_simulation(
        first_position_event.xyz,
        first_position_event.frame,
        parameter.frame_parameter,
        parameter.takeoff_parameter,
    )
    first_theorical_positions = linear_interpolation(
        first_position_event.xyz,
        second_position_event.xyz,
        int(
            parameter.takeoff_parameter.takeoff_elevation_duration_second
            * parameter.frame_parameter.position_fps
        ),
    )
    second_theorical_positions = linear_interpolation(
        second_position_event.xyz,
        second_position_event.xyz,
        int(
            parameter.takeoff_parameter.takeoff_stabilisation_duration_second
            * parameter.frame_parameter.position_fps
        ),
    )
    theorical_positions = first_theorical_positions + second_theorical_positions
    theorical_takeoff_simulation_infos = [
        SimulationInfo(
            first_position_event.frame + frame_index, theorical_position, True, False
        )
        for frame_index, theorical_position in enumerate(theorical_positions)
    ]
    assert len(real_takeoff_simulation_infos) == len(theorical_takeoff_simulation_infos)
    assert all(
        [
            real_takeoff_simulation_info == theorical_takeoff_simulation_info
            for real_takeoff_simulation_info, theorical_takeoff_simulation_info in zip(
                real_takeoff_simulation_infos, theorical_takeoff_simulation_infos
            )
        ]
    )
