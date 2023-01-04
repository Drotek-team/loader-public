import numpy as np
import pytest

from ...parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ...parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from ...show_dev.show_dev import DroneDev, PositionEventDev, ShowDev
from ...show_trajectory_collision.show_trajectory_collision import (
    ShowTrajectoryCollision,
)
from ..migration_SD_ST.SD_to_STC_procedure import SD_to_STC_procedure
from .STC_to_SSC_procedure import STC_to_SS_procedure

# @pytest.fixture
# def valid_show_trajectory_collision() -> ShowTrajectoryCollision:
#     FIRST_FRAME = 0
#     FIRST_POSITION = (5.36, 23.3, 24.1)

#     SECOND_FRAME = 1
#     SECOND_POSITION = (56, 98.54, 0.1854)
#     first_drone_trajectory_collision = DroneTrajectoryCollision(
#         0,
#         [
#             TrajectoryCollisionInfo(FIRST_FRAME, np.array(FIRST_POSITION), True),
#             TrajectoryCollisionInfo(SECOND_FRAME, np.array(SECOND_POSITION), True),
#         ],
#     )
#     second_drone_trajectory_collision = DroneTrajectoryCollision(
#         0,
#         [
#             TrajectoryCollisionInfo(FIRST_FRAME, np.array(FIRST_POSITION), True),
#             TrajectoryCollisionInfo(SECOND_FRAME, np.array(SECOND_POSITION), True),
#         ],
#     )
#     return ShowTrajectoryCollision(
#         [first_drone_trajectory_collision, second_drone_trajectory_collision]
#     )


@pytest.fixture
def valid_show_trajectory_collision() -> ShowTrajectoryCollision:

    drone_dev = DroneDev(
        0,
        [
            PositionEventDev(0, (0, 0, 0)),
            PositionEventDev(
                int(
                    TAKEOFF_PARAMETER.takeoff_duration_second
                    * FRAME_PARAMETER.position_fps
                ),
                (
                    0,
                    0,
                    TAKEOFF_PARAMETER.takeoff_altitude_meter,
                ),
            ),
        ],
    )
    show_dev = ShowDev([drone_dev])
    return SD_to_STC_procedure(
        show_dev,
    )


def test_valid_show_flags(valid_show_trajectory_collision: ShowTrajectoryCollision):

    show_simulation = STC_to_SS_procedure(valid_show_trajectory_collision)

    assert len(show_simulation.show_slices) == 53
    assert np.array_equal(
        show_simulation.show_slices[0].positions[0], np.array([0.0, 0.0, 0.0])
    )
    assert np.array_equal(
        show_simulation.show_slices[40].positions[0],
        np.array([0.0, 0.0, TAKEOFF_PARAMETER.takeoff_altitude_meter]),
    )
    assert np.array_equal(
        show_simulation.show_slices[41].positions[0],
        np.array([0.0, 0.0, TAKEOFF_PARAMETER.takeoff_altitude_meter]),
    )
    assert np.array_equal(
        show_simulation.show_slices[52].positions[0],
        np.array([0.0, 0.0, 0.0]),
    )
