from typing import Tuple

import numpy as np
from hypothesis import example, given
from hypothesis import strategies as st
from loader.parameters import FRAME_PARAMETERS, TAKEOFF_PARAMETERS
from loader.schemas.show_user import PositionEventUser
from loader.schemas.show_user.show_position_frame.simulation.position_simulation import (
    SimulationInfo,
)
from loader.schemas.show_user.show_position_frame.simulation.takeoff_simulation import (
    takeoff_simulation,
)

from tests.strategies import slow

FRAME_START = 0
FRAME_END = FRAME_START + FRAME_PARAMETERS.from_second_to_frame(
    TAKEOFF_PARAMETERS.takeoff_duration_second,
)
POSITION_START = (0.0, 0.0, 0.0)


def get_valid_position_events_user(
    takeoff_end_altitude: float,
) -> Tuple[PositionEventUser, PositionEventUser]:
    return PositionEventUser(frame=FRAME_START, xyz=POSITION_START), PositionEventUser(
        frame=FRAME_END,
        xyz=(
            POSITION_START[0],
            POSITION_START[1],
            POSITION_START[2] + takeoff_end_altitude,
        ),
    )


@given(
    takeoff_end_altitude=st.floats(
        TAKEOFF_PARAMETERS.takeoff_altitude_meter_min,
        TAKEOFF_PARAMETERS.takeoff_altitude_meter_max,
    ),
)
@example(2.0)
@slow
def test_takeoff_simulation_altitude_meter_min(takeoff_end_altitude: float) -> None:
    valid_position_events_user = get_valid_position_events_user(takeoff_end_altitude)
    first_position_event = valid_position_events_user[0]

    takeoff_simulation_infos = takeoff_simulation(
        first_position_event.xyz,
        takeoff_end_altitude,
        first_position_event.frame,
    )
    position_middle = (
        POSITION_START[0],
        POSITION_START[1],
        POSITION_START[2] + TAKEOFF_PARAMETERS.takeoff_altitude_meter_min,
    )
    position_end = (
        POSITION_START[0],
        POSITION_START[1],
        POSITION_START[2] + takeoff_end_altitude,
    )
    assert len(takeoff_simulation_infos) == 240
    assert takeoff_simulation_infos[0] == SimulationInfo(
        frame=0,
        position=np.array(POSITION_START),
    )
    assert takeoff_simulation_infos[72] == SimulationInfo(
        frame=72,
        position=np.array(position_middle),
    )
    assert takeoff_simulation_infos[239].frame == 239
    np.testing.assert_allclose(
        takeoff_simulation_infos[239].position,
        np.array(position_end),
        rtol=1e-2,
    )
