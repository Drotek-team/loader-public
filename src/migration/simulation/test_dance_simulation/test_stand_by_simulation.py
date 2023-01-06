from typing import Tuple

import numpy as np
import pytest

from ....parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ....show_user.show_user import PositionEventUser
from ...simulation.stand_by_simulation import stand_by_simulation
from ..position_simulation import SimulationInfo


@pytest.fixture
def valid_position_events_user() -> Tuple[PositionEventUser, PositionEventUser]:
    FRAME_START = 0
    FRAME_END = 20
    POSITION = (0.0, 0.0, 10.0)
    return PositionEventUser(
        position_frame=FRAME_START,
        absolute_time=FRAME_PARAMETER.from_position_frame_to_absolute_time(FRAME_START),
        xyz=POSITION,
    ), PositionEventUser(
        position_frame=FRAME_END,
        absolute_time=FRAME_PARAMETER.from_position_frame_to_absolute_time(FRAME_END),
        xyz=POSITION,
    )


def test_stand_by_simulation(
    valid_position_events_user: Tuple[PositionEventUser, PositionEventUser]
):

    first_position_event, second_position_event = (
        valid_position_events_user[0],
        valid_position_events_user[1],
    )
    real_stand_by_simulation_infos = stand_by_simulation(
        first_position_event.position_frame,
        second_position_event.position_frame,
        first_position_event.xyz,
    )

    theorical_stand_by_simulation_infos = [
        SimulationInfo(
            first_position_event.position_frame + frame_index,
            np.array(first_position_event.xyz),
            False,
            False,
        )
        for frame_index in range(
            second_position_event.position_frame - first_position_event.position_frame
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
