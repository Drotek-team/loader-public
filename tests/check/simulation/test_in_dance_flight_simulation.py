from typing import List

import numpy as np
import pytest
from loader.check.simulation.in_dance_flight_simulation import (
    in_dance_flight_simulation,
)
from loader.check.simulation.position_simulation import SimulationInfo
from loader.show_env.show_user.show_user import PositionEventUser


@pytest.fixture
def valid_position_events_user() -> List[PositionEventUser]:
    return [
        PositionEventUser(frame=0, xyz=(0.0, 2.0, 0.0)),
        PositionEventUser(frame=1, xyz=(2.0, 4.0, 1.0)),
        PositionEventUser(frame=3, xyz=(4.0, 8.0, 2.0)),
    ]


def test_in_air_flight_simulation(
    valid_position_events_user: List[PositionEventUser],
) -> None:
    real_in_air_flight_simulation_infos = in_dance_flight_simulation(
        valid_position_events_user,
    )
    theorical_in_air_flight_simulation_infos = [
        SimulationInfo(
            frame=0,
            position=np.array((0.0, 2.0, 0.0), dtype=np.float64),
            in_air=True,
        ),
        SimulationInfo(
            frame=1,
            position=np.array((2.0, 4.0, 1.0), dtype=np.float64),
            in_air=True,
        ),
        SimulationInfo(
            frame=2,
            position=np.array((3.0, 6.0, 1.5), dtype=np.float64),
            in_air=True,
        ),
    ]
    assert (
        real_in_air_flight_simulation_infos == theorical_in_air_flight_simulation_infos
    )