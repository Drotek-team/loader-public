from typing import List

import numpy as np
import pytest

from ...show_env.show_user.show_user import PositionEventUser
from .in_dance_flight_simulation import in_dance_flight_simulation
from .position_simulation import SimulationInfo


@pytest.fixture
def valid_position_events_user() -> List[PositionEventUser]:
    return [
        PositionEventUser(frame=0, xyz=(0.0, 0.0, 0.0)),
        PositionEventUser(frame=1, xyz=(0.0, 0.0, 1.0)),
        PositionEventUser(frame=3, xyz=(0.0, 0.0, 2.0)),
    ]


# TODO: remplir les champs x et y par acquis de conscience
def test_in_air_flight_simulation(valid_position_events_user: List[PositionEventUser]):
    real_in_air_flight_simulation_infos = in_dance_flight_simulation(
        valid_position_events_user,
    )
    theorical_in_air_flight_simulation_infos = [
        SimulationInfo(
            frame=0,
            position=np.array((0.0, 0.0, 0.0)),
            in_air=True,
        ),
        SimulationInfo(
            frame=1,
            position=np.array((0.0, 0.0, 1.0)),
            in_air=True,
        ),
        SimulationInfo(
            frame=2,
            position=np.array((0.0, 0.0, 1.5)),
            in_air=True,
        ),
    ]
    assert (
        real_in_air_flight_simulation_infos == theorical_in_air_flight_simulation_infos
    )
