from typing import Tuple

import pytest

from src.migration.migration_SD_ST.simulation.position_simulation import SimulationInfo

from .....parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from .....parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from .....show_dev.show_dev import PositionEventDev
from ...simulation.takeoff_simulation import takeoff_simulation
from ..in_air_flight_simulation import linear_interpolation


@pytest.fixture
def valid_position_events_dev() -> Tuple[PositionEventDev, PositionEventDev]:

    FRAME_START = 0
    POSITION = (0.0, 0.0, 0.0)
    return PositionEventDev(FRAME_START, POSITION), PositionEventDev(
        FRAME_START
        + int(FRAME_PARAMETER.absolute_fps * TAKEOFF_PARAMETER.takeoff_duration_second),
        (
            POSITION[0],
            POSITION[1],
            POSITION[2] + TAKEOFF_PARAMETER.takeoff_altitude_meter,
        ),
    )


def test_takeoff_simulation(
    valid_position_events_dev: Tuple[PositionEventDev, PositionEventDev]
):

    first_position_event, second_position_event = (
        valid_position_events_dev[0],
        valid_position_events_dev[1],
    )
    real_takeoff_simulation_infos = takeoff_simulation(
        first_position_event.xyz,
        first_position_event.frame,
    )
    first_theorical_positions = linear_interpolation(
        first_position_event.xyz,
        second_position_event.xyz,
        int(
            TAKEOFF_PARAMETER.takeoff_elevation_duration_second
            * FRAME_PARAMETER.position_fps
        ),
    )
    second_theorical_positions = linear_interpolation(
        second_position_event.xyz,
        second_position_event.xyz,
        int(
            TAKEOFF_PARAMETER.takeoff_stabilisation_duration_second
            * FRAME_PARAMETER.position_fps
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
