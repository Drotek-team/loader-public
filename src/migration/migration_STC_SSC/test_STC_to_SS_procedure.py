from ...show_trajectory_collision.show_trajectory_collision import (
    DroneTrajectoryCollision,
    ShowTrajectoryCollision,
    TrajectoryCollisionInfo,
)
import numpy as np
from .STC_to_SSC_procedure import STC_to_SS_procedure
import pytest
from ...parameter.parameter import Parameter
from ...show_simulation.show_simulation import ShowSimulation
import os
from ...show_dev.show_dev import DroneDev, PositionEventDev, ShowDev
from ..migration_SD_ST.SD_to_STC_procedure import SD_to_STC_procedure


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
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())

    drone_dev = DroneDev(
        0,
        [
            PositionEventDev(0, (0, 0, 0)),
            PositionEventDev(
                parameter.takeoff_parameter.takeoff_duration_second
                * parameter.frame_parameter.position_fps,
                (
                    0,
                    0,
                    parameter.takeoff_parameter.takeoff_altitude_meter,
                ),
            ),
        ],
    )
    show_dev = ShowDev([drone_dev])
    return SD_to_STC_procedure(
        show_dev,
        parameter.frame_parameter,
        parameter.takeoff_parameter,
        parameter.land_parameter,
    )


def test_valid_show_flags(valid_show_trajectory_collision: ShowTrajectoryCollision):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    show_simulation = STC_to_SS_procedure(valid_show_trajectory_collision)

    assert len(show_simulation.show_slices) == 52
    assert np.array_equal(
        show_simulation.show_slices[0].positions[0], np.array([0.0, 0.0, 0.0])
    )
    assert np.array_equal(
        show_simulation.show_slices[40].positions[0],
        np.array([0.0, 0.0, parameter.takeoff_parameter.takeoff_altitude_meter]),
    )
    assert np.array_equal(
        show_simulation.show_slices[41].positions[0],
        np.array([0.0, 0.0, parameter.takeoff_parameter.takeoff_altitude_meter]),
    )
    assert np.array_equal(
        show_simulation.show_slices[51].positions[0],
        np.array([0.0, 0.0, 0.0]),
    )
