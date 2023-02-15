from typing import Tuple

import numpy as np
import pytest
from loader.report.simulation.position_simulation import SimulationInfo
from loader.report.simulation.stand_by_simulation import stand_by_simulation
from loader.show_env.show_user import PositionEventUser


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

    theorical_stand_by_simulation_infos = [
        SimulationInfo(
            frame=0,
            position=np.array((0.0, 0.0, 10.0), dtype=np.float64),
            in_air=False,
        ),
        SimulationInfo(
            frame=1,
            position=np.array((0.0, 0.0, 10.0), dtype=np.float64),
            in_air=False,
        ),
        SimulationInfo(
            frame=2,
            position=np.array((0.0, 0.0, 10.0), dtype=np.float64),
            in_air=False,
        ),
    ]
    assert real_stand_by_simulation_infos == theorical_stand_by_simulation_infos
