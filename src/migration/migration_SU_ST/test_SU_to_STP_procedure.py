import numpy as np
import pytest

from ...parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ...parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from ...show_user.show_user import *
from .SU_to_STP_procedure import SU_to_STP_procedure


@pytest.fixture
def valid_show_user() -> ShowUser:
    drone_user = DroneUser(
        position_events=[
            PositionEventUser(position_frame=0, absolute_frame=0, xyz=(0.0, 0.0, 0.0)),
            PositionEventUser(
                position_frame=int(
                    FRAME_PARAMETER.position_fps
                    * TAKEOFF_PARAMETER.takeoff_duration_second
                ),
                absolute_frame=int(
                    FRAME_PARAMETER.absolute_fps
                    * TAKEOFF_PARAMETER.takeoff_duration_second
                ),
                xyz=(0.0, 0.0, TAKEOFF_PARAMETER.takeoff_altitude_meter),
            ),
            PositionEventUser(
                position_frame=int(
                    FRAME_PARAMETER.position_fps
                    * TAKEOFF_PARAMETER.takeoff_duration_second
                )
                + 1,
                absolute_frame=int(
                    FRAME_PARAMETER.absolute_fps
                    * TAKEOFF_PARAMETER.takeoff_duration_second
                )
                + 4,
                xyz=(0.0, 0.0, TAKEOFF_PARAMETER.takeoff_altitude_meter),
            ),
        ],
        color_events=[],
        fire_events=[],
    )
    return ShowUser(drones_user=[drone_user])


# TO DO: Quite a few more test is needed, for instance check the velocity/acceleration at the beggining are calculated according to the convention
def test_SU_to_STP_procedure(valid_show_user: ShowUser):
    show_trajectory_performance = SU_to_STP_procedure(valid_show_user)
    drone_trajectory_performance = (
        show_trajectory_performance.drones_trajectory_performance[0]
    )
    assert len(drone_trajectory_performance.trajectory_performance_infos) == 2
    first_trajectory_performance, second_trajectory_performance = (
        drone_trajectory_performance.trajectory_performance_infos[0],
        drone_trajectory_performance.trajectory_performance_infos[1],
    )
    assert (
        first_trajectory_performance.frame
        == FRAME_PARAMETER.from_second_to_position_frame(
            TAKEOFF_PARAMETER.takeoff_duration_second
        )
    )
    assert np.array_equal(
        first_trajectory_performance.position,
        np.array(
            (
                0.0,
                0.0,
                TAKEOFF_PARAMETER.takeoff_altitude_meter,
            )
        ),
    )

    assert (
        second_trajectory_performance.frame
        == FRAME_PARAMETER.from_second_to_position_frame(
            TAKEOFF_PARAMETER.takeoff_duration_second
        )
        + 1
    )
    assert np.array_equal(
        second_trajectory_performance.position,
        np.array(
            (
                0.0,
                0.0,
                TAKEOFF_PARAMETER.takeoff_altitude_meter,
            )
        ),
    )
