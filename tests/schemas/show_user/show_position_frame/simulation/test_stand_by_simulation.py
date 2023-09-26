from typing import Tuple

import numpy as np
import pytest
from loader.schemas.show_user import PositionEventUser
from loader.schemas.show_user.show_position_frame.simulation.position_simulation import (
    SimulationInfo,
)
from loader.schemas.show_user.show_position_frame.simulation.stand_by_simulation import (
    stand_by_simulation,
)


@pytest.fixture
def valid_position_events_user() -> Tuple[PositionEventUser, PositionEventUser]:
    return PositionEventUser(frame=0, xyz=(0.0, 0.0, 10.0)), PositionEventUser(
        frame=3,
        xyz=(0.0, 0.0, 10.0),
    )


def test_stand_by_simulation(
    valid_position_events_user: Tuple[PositionEventUser, PositionEventUser],
) -> None:
    first_position_event, second_position_event = (
        valid_position_events_user[0],
        valid_position_events_user[1],
    )
    real_stand_by_simulation_infos = stand_by_simulation(
        first_position_event.frame,
        second_position_event.frame,
        first_position_event.xyz,
    )

    assert real_stand_by_simulation_infos[0] == SimulationInfo(
        frame=0,
        position=np.array((0.0, 0.0, 10.0), dtype=np.float64),
    )
    assert real_stand_by_simulation_infos[1] == SimulationInfo(
        frame=1,
        position=np.array((0.0, 0.0, 10.0), dtype=np.float64),
    )
    assert real_stand_by_simulation_infos[2] == SimulationInfo(
        frame=2,
        position=np.array((0.0, 0.0, 10.0), dtype=np.float64),
    )


def test_stand_by_simulation_frame_begin_superior_to_frame_end(
    valid_position_events_user: Tuple[PositionEventUser, PositionEventUser],
) -> None:
    first_position_event, second_position_event = (
        valid_position_events_user[0],
        valid_position_events_user[1],
    )
    with pytest.raises(
        ValueError,
        match=f"frame end {first_position_event.frame} must be at least equal to frame begin {second_position_event.frame}",
    ):
        stand_by_simulation(
            second_position_event.frame,
            first_position_event.frame,
            first_position_event.xyz,
        )
