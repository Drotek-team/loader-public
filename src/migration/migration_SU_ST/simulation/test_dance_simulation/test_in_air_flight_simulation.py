from typing import List

import numpy as np
import pytest

from .....show_user.show_user import PositionEventUser
from ..in_air_flight_simulation import in_air_flight_simulation, linear_interpolation
from ..position_simulation import SimulationInfo


@pytest.fixture
def valid_position_events_user() -> List[PositionEventUser]:
    return [
        PositionEventUser(position_frame=0, absolute_time=0, xyz=(0, 0, 0)),
        PositionEventUser(position_frame=1, absolute_time=6, xyz=(0, 0, 1)),
        PositionEventUser(position_frame=4, absolute_time=24, xyz=(0, 0, 2)),
    ]


def test_flight_simulation(valid_position_events_user: List[PositionEventUser]):
    first_position_event_user, second_position_event_user, third_position_event_user = (
        valid_position_events_user[0],
        valid_position_events_user[1],
        valid_position_events_user[2],
    )
    real_in_air_flight_simulation_infos = in_air_flight_simulation(
        valid_position_events_user,
    )
    first_theorical_positions = linear_interpolation(
        first_position_event_user.xyz,
        second_position_event_user.xyz,
        second_position_event_user.position_frame
        - first_position_event_user.position_frame,
    )
    second_theorical_positions = linear_interpolation(
        second_position_event_user.xyz,
        third_position_event_user.xyz,
        third_position_event_user.position_frame
        - second_position_event_user.position_frame,
    )
    theorical_positions = (
        first_theorical_positions
        + second_theorical_positions
        + [np.array(third_position_event_user.xyz)]
    )
    theorical_in_air_flight_simulation_infos = [
        SimulationInfo(
            first_position_event_user.position_frame + frame_index,
            theorical_position,
            True,
            True,
        )
        for frame_index, theorical_position in enumerate(theorical_positions)
    ]
    assert len(real_in_air_flight_simulation_infos) == len(
        theorical_in_air_flight_simulation_infos
    )
    assert all(
        [
            real_in_air_flight_simulation_info
            == theorical_in_air_flight_simulation_info
            for real_in_air_flight_simulation_info, theorical_in_air_flight_simulation_info in zip(
                real_in_air_flight_simulation_infos,
                theorical_in_air_flight_simulation_infos,
            )
        ]
    )