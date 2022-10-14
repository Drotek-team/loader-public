import os
import numpy as np
from ...parameter.parameter import Parameter

import pytest
from ...show_trajectory_performance.show_trajectory_performance import (
    ShowTrajectoryPerformance,
)
from ...show_dev.show_dev import DroneDev, PositionEventDev, ShowDev
from ...migration.migration_SD_ST.SD_to_STP_procedure import SD_to_STP_procedure
from .show_trajectory_performance_check_report import (
    ShowTrajectoryPerformanceCheckReport,
)
from .show_trajectory_performance_check_procedure import (
    apply_show_trajectory_performance_check_procedure,
)

EPSILON_DELTA = 1e-3


@pytest.fixture
def valid_show_trajectory_performance() -> ShowTrajectoryPerformance:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())

    drone_dev = DroneDev(
        0,
        [
            PositionEventDev(0, (0.0, 0.0, 0.0)),
            PositionEventDev(
                parameter.takeoff_parameter.takeoff_duration_second
                * parameter.frame_parameter.position_fps,
                (
                    0.0,
                    0.0,
                    parameter.takeoff_parameter.takeoff_altitude_meter,
                ),
            ),
            PositionEventDev(
                parameter.takeoff_parameter.takeoff_duration_second
                * parameter.frame_parameter.position_fps
                + 1,
                (
                    0.0,
                    0.0,
                    parameter.takeoff_parameter.takeoff_altitude_meter,
                ),
            ),
        ],
    )
    return SD_to_STP_procedure(
        ShowDev([drone_dev]),
        parameter.frame_parameter,
    )


def test_valid_simulation(valid_show_trajectory_performance: ShowTrajectoryPerformance):
    show_trajectory_performance_check_report = ShowTrajectoryPerformanceCheckReport(
        valid_show_trajectory_performance.nb_drones
    )
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    apply_show_trajectory_performance_check_procedure(
        valid_show_trajectory_performance,
        show_trajectory_performance_check_report,
    )
    assert show_trajectory_performance_check_report.validation


# ROUNDING_ERROR = 0.04


# def test_invalid_horizontal_velocity_simulation():
#     parameter = Parameter()
#     parameter.load_parameter(os.getcwd())
#     distance_max = (
#         parameter.iostar_parameter.horizontal_velocity_max
#         * parameter.frame_parameter.position_rate_second
#     )
#     position_event_1 = PositionEvent(6, distance_max + ROUNDING_ERROR, 0, 0)
#     valid_show_simulation = get_show_simulation([position_event_1])
#     simulation_check_report = ShowSimulationCollisionCheckReport()
#     simulation_check_report.performance_check_report = PerformanceCheckReport(
#         valid_show_simulation.frames
#     )
#     apply_performance_check_procedure(
#         valid_show_simulation,
#         simulation_check_report.performance_check_report,
#         parameter.iostar_parameter,
#         parameter.takeoff_parameter,
#     )
#     assert not (
#         simulation_check_report.performance_check_report.performance_slices_check_report[
#             41
#         ].horizontal_velocity_check_report.validation
#     )


# def test_valid_horizontal_velocity_limitatition_simulation():
#     parameter = Parameter()
#     parameter.load_parameter(os.getcwd())
#     distance_max = (
#         parameter.iostar_parameter.horizontal_velocity_max
#         * parameter.frame_parameter.position_rate_second
#     )
#     position_event_1 = PositionEvent(6, distance_max - EPSILON_DELTA, 0, 0)

#     valid_show_simulation = get_show_simulation([position_event_1])
#     simulation_check_report = ShowSimulationCollisionCheckReport()
#     simulation_check_report.performance_check_report = PerformanceCheckReport(
#         valid_show_simulation.frames
#     )
#     apply_performance_check_procedure(
#         valid_show_simulation,
#         simulation_check_report.performance_check_report,
#         parameter.iostar_parameter,
#         parameter.takeoff_parameter,
#     )
#     assert simulation_check_report.performance_check_report.performance_slices_check_report[
#         41
#     ].horizontal_velocity_check_report.validation


# def test_invalid_horizontal_acceleration_simulation():
#     parameter = Parameter()
#     parameter.load_parameter(os.getcwd())
#     distance_max = (
#         parameter.iostar_parameter.horizontal_acceleration_max
#         * parameter.frame_parameter.position_rate_second
#         * parameter.frame_parameter.position_rate_second
#     )
#     position_event_1 = PositionEvent(6, distance_max + ROUNDING_ERROR, 0, 0)
#     valid_show_simulation = get_show_simulation([position_event_1])
#     simulation_check_report = ShowSimulationCollisionCheckReport()
#     simulation_check_report.performance_check_report = PerformanceCheckReport(
#         valid_show_simulation.frames
#     )
#     apply_performance_check_procedure(
#         valid_show_simulation,
#         simulation_check_report.performance_check_report,
#         parameter.iostar_parameter,
#         parameter.takeoff_parameter,
#     )
#     assert not (
#         simulation_check_report.performance_check_report.performance_slices_check_report[
#             41
#         ].horizontal_acceleration_check_report.validation
#     )


# def test_invalid_horizontal_acceleration_limitation_simulation():
#     parameter = Parameter()
#     parameter.load_parameter(os.getcwd())
#     distance_max = (
#         parameter.iostar_parameter.horizontal_acceleration_max
#         * parameter.frame_parameter.position_rate_second
#         * parameter.frame_parameter.position_rate_second
#     )
#     position_event_1 = PositionEvent(6, distance_max - EPSILON_DELTA, 0, 0)
#     valid_show_simulation = get_show_simulation([position_event_1])
#     simulation_check_report = ShowSimulationCollisionCheckReport()
#     simulation_check_report.performance_check_report = PerformanceCheckReport(
#         valid_show_simulation.frames
#     )
#     apply_performance_check_procedure(
#         valid_show_simulation,
#         simulation_check_report.performance_check_report,
#         parameter.iostar_parameter,
#         parameter.takeoff_parameter,
#     )
#     assert simulation_check_report.performance_check_report.performance_slices_check_report[
#         41
#     ].horizontal_acceleration_check_report.validation


# def test_invalid_up_force_simulation():
#     parameter = Parameter()
#     parameter.load_parameter(os.getcwd())
#     distance_max = parameter.frame_parameter.position_fps * np.sqrt(
#         parameter.iostar_parameter.force_up_max
#         / parameter.iostar_parameter.iostar_drag_vertical_coef
#     )
#     position_event_1 = PositionEvent(
#         6,
#         0,
#         0,
#         distance_max,
#     )
#     position_event_2 = PositionEvent(
#         12,
#         0,
#         0,
#         2 * distance_max,
#     )
#     position_event_3 = PositionEvent(
#         18,
#         0,
#         0,
#         2 * distance_max + EPSILON_DELTA,
#     )
#     valid_show_simulation = get_show_simulation(
#         [
#             position_event_1,
#             position_event_2,
#             position_event_3,
#         ]
#     )
#     simulation_check_report = ShowSimulationCollisionCheckReport()
#     simulation_check_report.performance_check_report = PerformanceCheckReport(
#         valid_show_simulation.frames
#     )
#     apply_performance_check_procedure(
#         valid_show_simulation,
#         simulation_check_report.performance_check_report,
#         parameter.iostar_parameter,
#         parameter.takeoff_parameter,
#     )
#     assert not (
#         simulation_check_report.performance_check_report.performance_slices_check_report[
#             42
#         ].up_force_check_report.validation
#     )