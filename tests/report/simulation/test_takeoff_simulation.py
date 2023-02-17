from typing import Tuple

import numpy as np
from hypothesis import example, given, settings
from hypothesis import strategies as st
from loader.parameter.iostar_dance_import_parameter.frame_parameter import (
    FRAME_PARAMETER,
)
from loader.parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from loader.report.simulation.position_simulation import (
    SimulationInfo,
)
from loader.report.simulation.takeoff_simulation import takeoff_simulation
from loader.show_env.show_user import PositionEventUser

FRAME_START = 0
FRAME_END = FRAME_START + FRAME_PARAMETER.from_second_to_frame(
    TAKEOFF_PARAMETER.takeoff_duration_second,
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
        TAKEOFF_PARAMETER.takeoff_altitude_meter_min,
        TAKEOFF_PARAMETER.takeoff_altitude_meter_max,
    ),
)
@example(2.0)
@settings(max_examples=50)
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
        POSITION_START[2] + TAKEOFF_PARAMETER.takeoff_altitude_meter_min,
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
        in_air=True,
    )
    assert takeoff_simulation_infos[72] == SimulationInfo(
        frame=72,
        position=np.array(position_middle),
        in_air=True,
    )
    assert takeoff_simulation_infos[239].frame == 239
    np.testing.assert_allclose(
        takeoff_simulation_infos[239].position,
        np.array(position_end),
        rtol=1e-2,
    )
    assert takeoff_simulation_infos[239].in_air
