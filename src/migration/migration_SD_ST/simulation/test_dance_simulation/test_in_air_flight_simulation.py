from typing import List

import numpy as np
import pytest

from .....show_dev.show_dev import PositionEventDev
from ..in_air_flight_simulation import in_air_flight_simulation, linear_interpolation
from ..position_simulation import SimulationInfo


@pytest.fixture
def valid_position_events_dev() -> List[PositionEventDev]:
    return [
        PositionEventDev(0, (0, 0, 0)),
        PositionEventDev(6, (0, 0, 1)),
        PositionEventDev(24, (0, 0, 2)),
    ]


def test_flight_simulation(valid_position_events_dev: List[PositionEventDev]):
    first_position_event_dev, second_position_event_dev, third_position_event_dev = (
        valid_position_events_dev[0],
        valid_position_events_dev[1],
        valid_position_events_dev[2],
    )
    real_in_air_flight_simulation_infos = in_air_flight_simulation(
        valid_position_events_dev,
    )
    first_theorical_positions = linear_interpolation(
        first_position_event_dev.xyz,
        second_position_event_dev.xyz,
        second_position_event_dev.frame - first_position_event_dev.frame,
    )
    second_theorical_positions = linear_interpolation(
        second_position_event_dev.xyz,
        third_position_event_dev.xyz,
        third_position_event_dev.frame - second_position_event_dev.frame,
    )
    theorical_positions = (
        first_theorical_positions
        + second_theorical_positions
        + [np.array(third_position_event_dev.xyz)]
    )
    theorical_in_air_flight_simulation_infos = [
        SimulationInfo(
            first_position_event_dev.frame + frame_index,
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
