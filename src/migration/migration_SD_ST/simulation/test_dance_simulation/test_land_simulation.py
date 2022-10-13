import os

import numpy as np

from .....parameter.parameter import Parameter
from ..in_air_flight_simulation import linear_interpolation
from ...simulation.land_simulation import land_simulation
import pytest
from .....show_dev.show_dev import PositionEventDev
from ..position_simulation import SimulationInfo

NUMERICAL_TOLERANCE = 1e-3


@pytest.fixture
def valid_position_event_dev_first_case() -> PositionEventDev:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    FRAME_START = 0
    POSITION_X = 2.36
    POSITION_Y = 5.69
    return PositionEventDev(
        FRAME_START,
        (
            POSITION_X,
            POSITION_Y,
            parameter.land_parameter.land_safe_hgt + NUMERICAL_TOLERANCE,
        ),
    )


@pytest.fixture
def valid_position_event_dev_second_case() -> PositionEventDev:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    FRAME_START = 0
    POSITION_X = 2.36
    POSITION_Y = 5.69
    return PositionEventDev(
        FRAME_START,
        (
            POSITION_X,
            POSITION_Y,
            parameter.land_parameter.land_safe_hgt - NUMERICAL_TOLERANCE,
        ),
    )


def test_land_simulation_first_case(
    valid_position_event_dev_first_case: PositionEventDev,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())

    real_land_simulation_infos = land_simulation(
        valid_position_event_dev_first_case.xyz,
        valid_position_event_dev_first_case.frame,
        parameter.frame_parameter,
        parameter.land_parameter,
    )
    land_middle_position = (
        valid_position_event_dev_first_case.xyz[0],
        valid_position_event_dev_first_case.xyz[1],
        parameter.land_parameter.get_second_land_altitude_start(
            valid_position_event_dev_first_case.xyz[2]
        ),
    )
    land_end_position = (
        valid_position_event_dev_first_case.xyz[0],
        valid_position_event_dev_first_case.xyz[1],
        0,
    )
    theorical_position = linear_interpolation(
        land_middle_position,
        land_end_position,
        int(
            parameter.land_parameter.get_second_land_second_delta(
                valid_position_event_dev_first_case.xyz[2]
            )
            * parameter.frame_parameter.position_fps
        ),
    )
    theorical_land_simulation_infos = [
        SimulationInfo(
            valid_position_event_dev_first_case.frame + frame_index,
            theorical_position,
            True,
            False,
        )
        for frame_index, theorical_position in enumerate(theorical_position)
    ]
    assert len(real_land_simulation_infos) == len(theorical_land_simulation_infos)
    assert all(
        [
            real_land_simulation_info == theorical_land_simulation_info
            for real_land_simulation_info, theorical_land_simulation_info in zip(
                real_land_simulation_infos, theorical_land_simulation_infos
            )
        ]
    )


def test_land_simulation_second_case(
    valid_position_event_dev_second_case: PositionEventDev,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())

    real_land_simulation_infos = land_simulation(
        valid_position_event_dev_second_case.xyz,
        valid_position_event_dev_second_case.frame,
        parameter.frame_parameter,
        parameter.land_parameter,
    )
    land_first_position = valid_position_event_dev_second_case.xyz
    land_middle_position = (
        valid_position_event_dev_second_case.xyz[0],
        valid_position_event_dev_second_case.xyz[1],
        parameter.land_parameter.get_second_land_altitude_start(
            valid_position_event_dev_second_case.xyz[2]
        ),
    )
    land_end_position = (
        valid_position_event_dev_second_case.xyz[0],
        valid_position_event_dev_second_case.xyz[1],
        0,
    )

    first_theorical_position = linear_interpolation(
        land_first_position,
        land_middle_position,
        int(
            parameter.land_parameter.get_first_land_second_delta(land_first_position[2])
            * parameter.frame_parameter.position_fps
        ),
    )
    second_theorical_position = linear_interpolation(
        land_middle_position,
        land_end_position,
        int(
            parameter.land_parameter.get_second_land_second_delta(
                land_middle_position[2]
            )
            * parameter.frame_parameter.position_fps
        ),
    )
    theorical_position = first_theorical_position + second_theorical_position
    theorical_land_simulation_infos = [
        SimulationInfo(
            valid_position_event_dev_second_case.frame + frame_index,
            theorical_position,
            True,
            False,
        )
        for frame_index, theorical_position in enumerate(theorical_position)
    ]
    assert len(real_land_simulation_infos) == len(theorical_land_simulation_infos)
    assert all(
        [
            real_land_simulation_info == theorical_land_simulation_info
            for real_land_simulation_info, theorical_land_simulation_info in zip(
                real_land_simulation_infos, theorical_land_simulation_infos
            )
        ]
    )
