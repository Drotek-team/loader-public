import pytest

from ...parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ...parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from ...parameter.iostar_physic_parameter import IOSTAR_PHYSIC_PARAMETER
from ...show_user.show_user import *
from .show_trajectory_performance_check_procedure import (
    apply_show_trajectory_performance_check_procedure,
)
from .show_trajectory_performance_check_report import (
    ShowTrajectoryPerformanceCheckReport,
)

EPSILON_DELTA = 1e-2


@pytest.fixture
def valid_show_user() -> ShowUser:
    drone_user = DroneUser(
        position_events=[
            PositionEventUser(frame=0, xyz=(0.0, 0.0, 0.0)),
            PositionEventUser(
                frame=FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
                    TAKEOFF_PARAMETER.takeoff_duration_second
                ),
                xyz=(
                    0.0,
                    0.0,
                    TAKEOFF_PARAMETER.takeoff_altitude_meter_min,
                ),
            ),
            PositionEventUser(
                frame=FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
                    TAKEOFF_PARAMETER.takeoff_duration_second
                )
                + 1,
                xyz=(
                    0.0,
                    0.0,
                    TAKEOFF_PARAMETER.takeoff_altitude_meter_min,
                ),
            ),
        ],
        color_events=[],
        fire_events=[],
    )
    return ShowUser(drones_user=[drone_user])


def test_valid_show_trajectory_performance(
    valid_show_user: ShowUser,
):
    show_trajectory_performance_check_report = ShowTrajectoryPerformanceCheckReport(
        valid_show_user.nb_drones
    )

    apply_show_trajectory_performance_check_procedure(
        valid_show_user,
        show_trajectory_performance_check_report,
    )
    assert show_trajectory_performance_check_report.validation


@pytest.fixture
def invalid_show_user_horizontal_velocity() -> ShowUser:
    drone_user = DroneUser(
        position_events=[
            PositionEventUser(frame=0, xyz=(0.0, 0.0, 0.0)),
            PositionEventUser(
                frame=FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
                    TAKEOFF_PARAMETER.takeoff_duration_second
                ),
                xyz=(
                    0.0,
                    0.0,
                    TAKEOFF_PARAMETER.takeoff_altitude_meter_min,
                ),
            ),
            PositionEventUser(
                frame=FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
                    TAKEOFF_PARAMETER.takeoff_duration_second
                )
                + 1,
                xyz=(
                    FRAME_PARAMETER.from_absolute_frame_to_absolute_time(
                        IOSTAR_PHYSIC_PARAMETER.horizontal_velocity_max
                    )
                    + EPSILON_DELTA,
                    0.0,
                    TAKEOFF_PARAMETER.takeoff_altitude_meter_min,
                ),
            ),
        ],
        color_events=[],
        fire_events=[],
    )
    return ShowUser(drones_user=[drone_user])


def test_invalid_show_user_horizontal_velocity(
    invalid_show_user_horizontal_velocity: ShowUser,
):
    show_trajectory_performance_check_report = ShowTrajectoryPerformanceCheckReport(
        invalid_show_user_horizontal_velocity.nb_drones
    )

    apply_show_trajectory_performance_check_procedure(
        invalid_show_user_horizontal_velocity,
        show_trajectory_performance_check_report,
    )
    performance_infractions = show_trajectory_performance_check_report.drones_trajectory_performance_check_report[
        0
    ].performance_infractions
    assert len(performance_infractions) >= 1
    assert (
        performance_infractions[0].name
        == "The performance horizontal velocity has the value: 6.24 (max: 6.0) at the frame 240"
    )


@pytest.fixture
def invalid_show_user_vertical_position() -> ShowUser:
    drone_user = DroneUser(
        position_events=[
            PositionEventUser(frame=0, xyz=(0.0, 0.0, 0.0)),
            PositionEventUser(
                frame=FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
                    TAKEOFF_PARAMETER.takeoff_duration_second
                ),
                xyz=(
                    0.0,
                    0.0,
                    TAKEOFF_PARAMETER.takeoff_altitude_meter_min,
                ),
            ),
            PositionEventUser(
                frame=FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
                    TAKEOFF_PARAMETER.takeoff_duration_second
                )
                + 1,
                xyz=(
                    0.0,
                    0.0,
                    TAKEOFF_PARAMETER.takeoff_altitude_meter_min - EPSILON_DELTA,
                ),
            ),
        ],
        color_events=[],
        fire_events=[],
    )
    return ShowUser(drones_user=[drone_user])


def test_invalid_show_user_vertical_position(
    invalid_show_user_vertical_position: ShowUser,
):
    show_trajectory_performance_check_report = ShowTrajectoryPerformanceCheckReport(
        invalid_show_user_vertical_position.nb_drones
    )

    apply_show_trajectory_performance_check_procedure(
        invalid_show_user_vertical_position,
        show_trajectory_performance_check_report,
    )
    performance_infractions = show_trajectory_performance_check_report.drones_trajectory_performance_check_report[
        0
    ].performance_infractions
    assert len(performance_infractions) >= 1
    assert (
        performance_infractions[0].name
        == "The performance vertical position has the value: 0.99 (min: 1.0) at the frame 240"
    )


@pytest.fixture
def invalid_show_user_velocity_up() -> ShowUser:
    drone_user = DroneUser(
        position_events=[
            PositionEventUser(frame=0, xyz=(0.0, 0.0, 0.0)),
            PositionEventUser(
                frame=FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
                    TAKEOFF_PARAMETER.takeoff_duration_second
                ),
                xyz=(
                    0.0,
                    0.0,
                    TAKEOFF_PARAMETER.takeoff_altitude_meter_min,
                ),
            ),
            PositionEventUser(
                frame=FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
                    TAKEOFF_PARAMETER.takeoff_duration_second
                )
                + 1,
                xyz=(
                    0.0,
                    0.0,
                    TAKEOFF_PARAMETER.takeoff_altitude_meter_min
                    + FRAME_PARAMETER.from_absolute_frame_to_absolute_time(
                        IOSTAR_PHYSIC_PARAMETER.velocity_up_max
                    )
                    + EPSILON_DELTA,
                ),
            ),
        ],
        color_events=[],
        fire_events=[],
    )
    return ShowUser(drones_user=[drone_user])


def test_invalid_show_user_velocity_up(
    invalid_show_user_velocity_up: ShowUser,
):
    show_trajectory_performance_check_report = ShowTrajectoryPerformanceCheckReport(
        invalid_show_user_velocity_up.nb_drones
    )

    apply_show_trajectory_performance_check_procedure(
        invalid_show_user_velocity_up,
        show_trajectory_performance_check_report,
    )
    performance_infractions = show_trajectory_performance_check_report.drones_trajectory_performance_check_report[
        0
    ].performance_infractions
    assert len(performance_infractions) >= 1
    assert (
        performance_infractions[0].name
        == "The performance up velocity has the value: 4.24 (max: 4.0) at the frame 240"
    )


@pytest.fixture
def invalid_show_user_velocity_down() -> ShowUser:
    drone_user = DroneUser(
        position_events=[
            PositionEventUser(frame=0, xyz=(0.0, 0.0, 0.0)),
            PositionEventUser(
                frame=FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
                    TAKEOFF_PARAMETER.takeoff_duration_second
                ),
                xyz=(
                    0.0,
                    0.0,
                    TAKEOFF_PARAMETER.takeoff_altitude_meter_min,
                ),
            ),
            PositionEventUser(
                frame=FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
                    TAKEOFF_PARAMETER.takeoff_duration_second
                )
                + 1,
                xyz=(
                    0.0,
                    0.0,
                    TAKEOFF_PARAMETER.takeoff_altitude_meter_min
                    - FRAME_PARAMETER.from_absolute_frame_to_absolute_time(
                        IOSTAR_PHYSIC_PARAMETER.velocity_down_max
                    )
                    - EPSILON_DELTA,
                ),
            ),
        ],
        color_events=[],
        fire_events=[],
    )
    return ShowUser(drones_user=[drone_user])


def test_invalid_show_user_velocity_down(
    invalid_show_user_velocity_down: ShowUser,
):
    show_trajectory_performance_check_report = ShowTrajectoryPerformanceCheckReport(
        invalid_show_user_velocity_down.nb_drones
    )

    apply_show_trajectory_performance_check_procedure(
        invalid_show_user_velocity_down,
        show_trajectory_performance_check_report,
    )
    performance_infractions = show_trajectory_performance_check_report.drones_trajectory_performance_check_report[
        0
    ].performance_infractions
    assert len(performance_infractions) >= 1
    assert (
        performance_infractions[1].name
        == "The performance down velocity has the value: 4.24 (max: 4.0) at the frame 240"
    )


@pytest.fixture
def invalid_show_user_acceleration() -> ShowUser:
    drone_user = DroneUser(
        position_events=[
            PositionEventUser(frame=0, xyz=(0.0, 0.0, 0.0)),
            PositionEventUser(
                frame=FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
                    TAKEOFF_PARAMETER.takeoff_duration_second
                ),
                xyz=(
                    0.0,
                    0.0,
                    TAKEOFF_PARAMETER.takeoff_altitude_meter_min,
                ),
            ),
            PositionEventUser(
                frame=FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
                    TAKEOFF_PARAMETER.takeoff_duration_second
                )
                + 1,
                xyz=(
                    0.0,
                    0.0,
                    TAKEOFF_PARAMETER.takeoff_altitude_meter_min
                    - FRAME_PARAMETER.from_absolute_frame_to_absolute_time(
                        IOSTAR_PHYSIC_PARAMETER.velocity_down_max
                    )
                    - EPSILON_DELTA,
                ),
            ),
        ],
        color_events=[],
        fire_events=[],
    )
    return ShowUser(drones_user=[drone_user])


def test_invalid_show_user_velocity_down(
    invalid_show_user_velocity_down: ShowUser,
):
    show_trajectory_performance_check_report = ShowTrajectoryPerformanceCheckReport(
        invalid_show_user_velocity_down.nb_drones
    )

    apply_show_trajectory_performance_check_procedure(
        invalid_show_user_velocity_down,
        show_trajectory_performance_check_report,
    )
    performance_infractions = show_trajectory_performance_check_report.drones_trajectory_performance_check_report[
        0
    ].performance_infractions
    assert len(performance_infractions) >= 1
    assert (
        performance_infractions[2].name
        == "The performance acceleration has the value: 101.76 (max: 2.0) at the frame 240"
    )
