from typing import Tuple

import numpy as np
import pytest

from .....show_dev.show_dev import PositionEventDev
from ...simulation.stand_by_simulation import stand_by_simulation
from ..position_simulation import SimulationInfo


@pytest.fixture
def valid_position_events_dev() -> Tuple[PositionEventDev, PositionEventDev]:
    FRAME_START = 0
    FRAME_END = 20
    POSITION = (0.0, 0.0, 10.0)
    return PositionEventDev(FRAME_START, POSITION), PositionEventDev(
        FRAME_END, POSITION
    )


def test_stand_by_simulation(
    valid_position_events_dev: Tuple[PositionEventDev, PositionEventDev]
):

    first_position_event, second_position_event = (
        valid_position_events_dev[0],
        valid_position_events_dev[1],
    )
    real_stand_by_simulation_infos = stand_by_simulation(
        first_position_event.frame,
        second_position_event.frame,
        first_position_event.xyz,
    )

    theorical_stand_by_simulation_infos = [
        SimulationInfo(
            first_position_event.frame + frame_index,
            np.array(first_position_event.xyz),
            False,
            False,
        )
        for frame_index in range(
            second_position_event.frame - first_position_event.frame
        )
    ]
    assert len(real_stand_by_simulation_infos) == len(
        theorical_stand_by_simulation_infos
    )
    assert all(
        [
            real_stand_by_simulation_info == theorical_stand_by_simulation_info
            for real_stand_by_simulation_info, theorical_stand_by_simulation_info in zip(
                real_stand_by_simulation_infos, theorical_stand_by_simulation_infos
            )
        ]
    )
