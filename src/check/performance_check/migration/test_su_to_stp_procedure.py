import numpy as np
import pytest

from ....parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ....parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from ....show_env.show_user.show_user import *
from .su_to_stp_procedure import su_to_stp_procedure


@pytest.fixture
def valid_show_user() -> ShowUser:
    drone_user = DroneUser(
        position_events=[
            PositionEventUser(frame=0, xyz=(0.0, 0.0, 0.0)),
            PositionEventUser(
                frame=FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
                    TAKEOFF_PARAMETER.takeoff_duration_second
                ),
                xyz=(0.0, 0.0, TAKEOFF_PARAMETER.takeoff_altitude_meter_min),
            ),
            PositionEventUser(
                frame=FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
                    TAKEOFF_PARAMETER.takeoff_duration_second
                )
                + 1,
                xyz=(0.0, 0.0, TAKEOFF_PARAMETER.takeoff_altitude_meter_min),
            ),
        ],
        color_events=[],
        fire_events=[],
    )
    return ShowUser(drones_user=[drone_user])


# TODO: Quite a few more test is needed, for instance check the velocity/acceleration at the beggining are calculated according to the convention
def test_su_to_stp_procedure(valid_show_user: ShowUser):
    show_trajectory_performance = su_to_stp_procedure(valid_show_user)
    drone_trajectory_performance = (
        show_trajectory_performance.drones_trajectory_performance[0]
    )
    assert len(drone_trajectory_performance.trajectory_performance_infos) == 2
    first_trajectory_performance, second_trajectory_performance = (
        drone_trajectory_performance.trajectory_performance_infos[0],
        drone_trajectory_performance.trajectory_performance_infos[1],
    )
    assert (
        first_trajectory_performance.frame + 1
        == FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
            TAKEOFF_PARAMETER.takeoff_duration_second
        )
    )
    assert np.array_equal(
        first_trajectory_performance.position,
        np.array(
            (
                0.0,
                0.0,
                TAKEOFF_PARAMETER.takeoff_altitude_meter_min,
            )
        ),
    )
    assert (
        second_trajectory_performance.frame
        == FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
            TAKEOFF_PARAMETER.takeoff_duration_second
        )
    )
    assert np.array_equal(
        second_trajectory_performance.position,
        np.array(
            (
                0.0,
                0.0,
                TAKEOFF_PARAMETER.takeoff_altitude_meter_min,
            )
        ),
    )
