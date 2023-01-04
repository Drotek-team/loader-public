import pytest

from ...migration.migration_SD_ST.SD_to_STP_procedure import SD_to_STP_procedure
from ...parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ...parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from ...parameter.iostar_physic_parameter import IOSTAR_PHYSIC_PARAMETER
from ...show_dev.show_dev import DroneDev, PositionEventDev, ShowDev
from ...show_trajectory_performance.show_trajectory_performance import (
    ShowTrajectoryPerformance,
)
from .show_trajectory_performance_check_procedure import (
    apply_show_trajectory_performance_check_procedure,
)
from .show_trajectory_performance_check_report import (
    ShowTrajectoryPerformanceCheckReport,
)

EPSILON_DELTA = 1e-2
ROUNDING_ERROR = 0.04


@pytest.fixture
def valid_show_trajectory_performance() -> ShowTrajectoryPerformance:

    drone_dev = DroneDev(
        0,
        [
            PositionEventDev(0, (0.0, 0.0, 0.0)),
            PositionEventDev(
                FRAME_PARAMETER.from_second_to_position_frame(
                    TAKEOFF_PARAMETER.takeoff_duration_second
                ),
                (
                    0.0,
                    0.0,
                    TAKEOFF_PARAMETER.takeoff_altitude_meter,
                ),
            ),
            PositionEventDev(
                FRAME_PARAMETER.from_second_to_position_frame(
                    TAKEOFF_PARAMETER.takeoff_duration_second
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
    return SD_to_STP_procedure(
        ShowDev([drone_dev]),
    )


def test_valid_show_trajectory_performance(
    valid_show_trajectory_performance: ShowTrajectoryPerformance,
):
    show_trajectory_performance_check_report = ShowTrajectoryPerformanceCheckReport(
        valid_show_trajectory_performance.nb_drones
    )

    apply_show_trajectory_performance_check_procedure(
        valid_show_trajectory_performance,
        show_trajectory_performance_check_report,
    )
    assert show_trajectory_performance_check_report.validation


@pytest.fixture
def invalid_show_trajectory_performance_horizontal_velocity() -> ShowTrajectoryPerformance:

    drone_dev = DroneDev(
        0,
        [
            PositionEventDev(0, (0.0, 0.0, 0.0)),
            PositionEventDev(
                FRAME_PARAMETER.from_second_to_position_frame(
                    TAKEOFF_PARAMETER.takeoff_duration_second
                ),
                (
                    0.0,
                    0.0,
                    TAKEOFF_PARAMETER.takeoff_altitude_meter,
                ),
            ),
            PositionEventDev(
                FRAME_PARAMETER.from_second_to_position_frame(
                    TAKEOFF_PARAMETER.takeoff_duration_second
                )
                + 1,
                (
                    IOSTAR_PHYSIC_PARAMETER.horizontal_velocity_max
                    / FRAME_PARAMETER.position_fps
                    + EPSILON_DELTA,
                    0.0,
                    TAKEOFF_PARAMETER.takeoff_altitude_meter,
                ),
            ),
        ],
    )
    return SD_to_STP_procedure(
        ShowDev([drone_dev]),
    )


# TO DO: validate the model with Raphael
def test_invalid_show_trajectory_performance_horizontal_velocity(
    invalid_show_trajectory_performance_horizontal_velocity: ShowTrajectoryPerformance,
):
    show_trajectory_performance_check_report = ShowTrajectoryPerformanceCheckReport(
        invalid_show_trajectory_performance_horizontal_velocity.nb_drones
    )

    apply_show_trajectory_performance_check_procedure(
        invalid_show_trajectory_performance_horizontal_velocity,
        show_trajectory_performance_check_report,
    )
    performance_infractions = show_trajectory_performance_check_report.drones_trajectory_performance_check_report[
        0
    ].performance_infractions
    assert len(performance_infractions) == 2
    first_performance_infraction = performance_infractions[0]
    assert first_performance_infraction.performance_name == "horizontal velocity"
    assert (
        first_performance_infraction.performance_value
        == IOSTAR_PHYSIC_PARAMETER.horizontal_velocity_max
        + EPSILON_DELTA * FRAME_PARAMETER.position_fps
    )
