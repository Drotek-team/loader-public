import numpy as np
import pytest

from ...parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ...parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from ...show_trajectory_collision.show_trajectory_collision import *
from ...show_user.show_user import DroneUser, PositionEventUser, ShowUser
from ..migration_SU_ST.SU_to_STC_procedure import SU_to_STC_procedure
from .STC_to_SSC_procedure import STC_to_SS_procedure


@pytest.fixture
def valid_show_trajectory() -> CollisionShowTrajectory:
    drone_user = DroneUser(
        position_events=[
            PositionEventUser(position_frame=0, absolute_time=0, xyz=(0.0, 0.0, 0.0)),
            PositionEventUser(
                position_frame=int(
                    FRAME_PARAMETER.position_fps
                    * TAKEOFF_PARAMETER.takeoff_duration_second
                ),
                absolute_time=TAKEOFF_PARAMETER.takeoff_duration_second,
                xyz=(0.0, 0.0, TAKEOFF_PARAMETER.takeoff_altitude_meter),
            ),
        ],
        color_events=[],
        fire_events=[],
    )
    show_user = ShowUser(drones_user=[drone_user])
    return SU_to_STC_procedure(
        show_user,
    )


def test_valid_show_flags(valid_show_trajectory: CollisionShowTrajectory):
    show_simulation = STC_to_SS_procedure(valid_show_trajectory)
    assert len(show_simulation.show_slices) == 51
    assert np.array_equal(
        show_simulation.show_slices[0].positions[0], np.array([0.0, 0.0, 0.0])
    )
    assert np.array_equal(show_simulation.show_slices[0].in_air_flags, np.array([True]))
    assert np.array_equal(
        show_simulation.show_slices[40].positions[0],
        np.array([0.0, 0.0, TAKEOFF_PARAMETER.takeoff_altitude_meter]),
    )
    assert np.array_equal(
        show_simulation.show_slices[50].positions[0],
        np.array([0.0, 0.0, 0.0]),
    )
