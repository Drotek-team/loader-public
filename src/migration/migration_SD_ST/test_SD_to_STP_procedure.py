import numpy as np
import pytest

from ...parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ...parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from ...show_dev.show_dev import DroneDev, PositionEventDev, ShowDev
from .SD_to_STP_procedure import SD_to_STP_procedure


@pytest.fixture
def valid_show_dev() -> ShowDev:

    drone_dev = DroneDev(
        0,
        [
            PositionEventDev(0, (0.0, 0.0, 0.0)),
            PositionEventDev(
                int(
                    TAKEOFF_PARAMETER.takeoff_duration_second
                    * FRAME_PARAMETER.position_fps
                ),
                (
                    0.0,
                    0.0,
                    TAKEOFF_PARAMETER.takeoff_altitude_meter,
                ),
            ),
            PositionEventDev(
                int(
                    TAKEOFF_PARAMETER.takeoff_duration_second
                    * FRAME_PARAMETER.position_fps
                )
                + 1,
                (
                    0.0,
                    0.0,
                    TAKEOFF_PARAMETER.takeoff_altitude_meter,
                ),
            ),
        ],
    )
    return ShowDev([drone_dev])


# TO DO: Quite a few more test is needed, for instance check the velocity/acceleration at the beggining are calculated according to the convention
def test_SD_to_STP_procedure(valid_show_dev: ShowDev):

    show_trajectory_performance = SD_to_STP_procedure(valid_show_dev)
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
        == TAKEOFF_PARAMETER.takeoff_duration_second * FRAME_PARAMETER.position_fps
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
        == TAKEOFF_PARAMETER.takeoff_duration_second * FRAME_PARAMETER.position_fps + 1
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
