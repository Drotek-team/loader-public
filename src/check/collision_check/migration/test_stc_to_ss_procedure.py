import numpy as np
import pytest

from ....parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ....parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from ....show_env.show_user.show_user import DroneUser, PositionEventUser, ShowUser
from .show_trajectory_collision import *
from .stc_to_ssc_procedure import stc_to_ss_procedure
from .su_to_stc_procedure import su_to_stc_procedure


@pytest.fixture
def valid_show_trajectory() -> CollisionShowTrajectory:
    drone_user = DroneUser(
        position_events=[
            PositionEventUser(frame=0, xyz=(0.0, 0.0, 0.0)),
            PositionEventUser(
                frame=FRAME_PARAMETER.from_second_to_frame(
                    TAKEOFF_PARAMETER.takeoff_duration_second
                ),
                xyz=(0.0, 0.0, TAKEOFF_PARAMETER.takeoff_altitude_meter_min),
            ),
        ],
        color_events=[],
        fire_events=[],
    )
    show_user = ShowUser(drones_user=[drone_user])
    return su_to_stc_procedure(
        show_user,
    )


def test_valid_show_flags(valid_show_trajectory: CollisionShowTrajectory):
    show_simulation = stc_to_ss_procedure(valid_show_trajectory)
    assert len(show_simulation.show_slices) == 301
    assert np.array_equal(
        show_simulation.show_slices[0].positions[0], np.array([0.0, 0.0, 0.0])
    )
    assert np.array_equal(show_simulation.show_slices[0].in_air_flags, np.array([True]))
    assert np.array_equal(
        show_simulation.show_slices[240].positions[0],
        np.array([0.0, 0.0, TAKEOFF_PARAMETER.takeoff_altitude_meter_min]),
    )
    assert np.array_equal(
        show_simulation.show_slices[-1].positions[0],
        np.array([0.0, 0.0, 0.0]),
    )
