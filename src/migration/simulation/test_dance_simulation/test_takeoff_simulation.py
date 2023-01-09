from typing import Tuple

import pytest

from ....parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ....parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from ....show_user.show_user import PositionEventUser
from ...simulation.takeoff_simulation import takeoff_simulation
from ..in_air_flight_simulation import linear_interpolation
from ..position_simulation import SimulationInfo


@pytest.fixture
def valid_position_events_user() -> Tuple[PositionEventUser, PositionEventUser]:

    FRAME_START = 0
    FRAME_END = FRAME_START + FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
        TAKEOFF_PARAMETER.takeoff_duration_second
    )
    POSITION = (0.0, 0.0, 0.0)
    return PositionEventUser(frame=FRAME_START, xyz=POSITION,), PositionEventUser(
        frame=FRAME_END,
        xyz=(
            POSITION[0],
            POSITION[1],
            POSITION[2] + TAKEOFF_PARAMETER.takeoff_altitude_meter_min,
        ),
    )


def test_takeoff_simulation(
    valid_position_events_user: Tuple[PositionEventUser, PositionEventUser]
):
    first_position_event, second_position_event = (
        valid_position_events_user[0],
        valid_position_events_user[1],
    )
    real_takeoff_simulation_infos = takeoff_simulation(
        first_position_event.xyz,
        first_position_event.position_frame,
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
        )
        - 1,
    )
    theorical_positions = first_theorical_positions + second_theorical_positions
    theorical_takeoff_simulation_infos = [
        SimulationInfo(
            first_position_event.position_frame + frame_index,
            theorical_position,
            True,
            False,
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
