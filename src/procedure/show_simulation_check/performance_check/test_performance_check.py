from multiprocessing.sharedctypes import Value
import os
from typing import List
import numpy as np
from ....show_px4.drone_px4.events.position_events import PositionEvent
from ....show_px4.show_px4 import DronePx4, ShowPx4
from ....parameter.parameter import Parameter
from .performance_check_procedure import (
    apply_performance_check_procedure,
)
from .performance_check_report import (
    PerformanceCheckReport,
)
from ....show_simulation.show_simulation import ShowSimulation
from ..simulation_check_report import (
    SimulationCheckReport,
)
from ...migration_DP_SS.SP_to_SS_procedure import DP_to_SS_procedure
from ...migration_SP_SU.data_convertion_format import XyzConvertionStandard

EPSILON_DELTA = 1e-3


def get_show_simulation(position_events: List[PositionEvent]) -> ShowSimulation:
    parameter = Parameter()
    xyz_convertion_standard = XyzConvertionStandard()
    parameter.load_parameter(os.getcwd())
    drone = DronePx4(0)
    drone.add_position(0, (0, 0, 0))
    drone.add_position(
        int(
            parameter.frame_parameter.json_fps
            * parameter.takeoff_parameter.takeoff_duration_second
        ),
        xyz_convertion_standard.from_user_xyz_to_px4_xyz(
            (0, 0, parameter.takeoff_parameter.takeoff_altitude_meter)
        ),
    )
    for position_event in position_events:
        position = position_event.xyz
        drone.add_position(
            int(
                parameter.frame_parameter.json_fps
                * parameter.takeoff_parameter.takeoff_duration_second
            )
            + position_event.frame,
            xyz_convertion_standard.from_user_xyz_to_px4_xyz(
                (
                    position[0],
                    position[1],
                    parameter.takeoff_parameter.takeoff_altitude_meter + position[2],
                )
            ),
        )

    show_px4 = ShowPx4([drone])
    show_simulation = DP_to_SS_procedure(
        show_px4,
        parameter.frame_parameter,
        parameter.takeoff_parameter,
        parameter.land_parameter,
    )
    return show_simulation


def test_valid_simulation():
    position_event_1 = PositionEvent(1, 0, 0, 0)
    position_event_2 = PositionEvent(2, 0, 0, 0)
    position_event_3 = PositionEvent(3, 0, 0, 0)
    valid_show_simulation = get_show_simulation(
        [position_event_1, position_event_2, position_event_3]
    )
    performance_check_report = PerformanceCheckReport()
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    apply_performance_check_procedure(
        valid_show_simulation,
        performance_check_report,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
    )
    assert performance_check_report.validation


ROUNDING_ERROR = 0.04


def test_invalid_horizontal_velocity_simulation():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    distance_max = (
        parameter.iostar_parameter.horizontal_velocity_max
        * parameter.frame_parameter.position_rate_second
    )
    position_event_1 = PositionEvent(6, distance_max + ROUNDING_ERROR, 0, 0)
    valid_show_simulation = get_show_simulation([position_event_1])
    simulation_check_report = SimulationCheckReport()
    simulation_check_report.performance_check_report = PerformanceCheckReport(
        valid_show_simulation.frames
    )
    apply_performance_check_procedure(
        valid_show_simulation,
        simulation_check_report.performance_check_report,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
    )
    assert not (
        simulation_check_report.performance_check_report.performance_slices_check_report[
            41
        ].horizontal_velocity_check_report.validation
    )


def test_valid_horizontal_velocity_limitatition_simulation():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    distance_max = (
        parameter.iostar_parameter.horizontal_velocity_max
        * parameter.frame_parameter.position_rate_second
    )
    position_event_1 = PositionEvent(6, distance_max - EPSILON_DELTA, 0, 0)

    valid_show_simulation = get_show_simulation([position_event_1])
    simulation_check_report = SimulationCheckReport()
    simulation_check_report.performance_check_report = PerformanceCheckReport(
        valid_show_simulation.frames
    )
    apply_performance_check_procedure(
        valid_show_simulation,
        simulation_check_report.performance_check_report,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
    )
    assert simulation_check_report.performance_check_report.performance_slices_check_report[
        41
    ].horizontal_velocity_check_report.validation


def test_invalid_horizontal_acceleration_simulation():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    distance_max = (
        parameter.iostar_parameter.horizontal_acceleration_max
        * parameter.frame_parameter.position_rate_second
        * parameter.frame_parameter.position_rate_second
    )
    position_event_1 = PositionEvent(6, distance_max + ROUNDING_ERROR, 0, 0)
    valid_show_simulation = get_show_simulation([position_event_1])
    simulation_check_report = SimulationCheckReport()
    simulation_check_report.performance_check_report = PerformanceCheckReport(
        valid_show_simulation.frames
    )
    apply_performance_check_procedure(
        valid_show_simulation,
        simulation_check_report.performance_check_report,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
    )
    assert not (
        simulation_check_report.performance_check_report.performance_slices_check_report[
            41
        ].horizontal_acceleration_check_report.validation
    )


def test_invalid_horizontal_acceleration_limitation_simulation():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    distance_max = (
        parameter.iostar_parameter.horizontal_acceleration_max
        * parameter.frame_parameter.position_rate_second
        * parameter.frame_parameter.position_rate_second
    )
    position_event_1 = PositionEvent(6, distance_max - EPSILON_DELTA, 0, 0)
    valid_show_simulation = get_show_simulation([position_event_1])
    simulation_check_report = SimulationCheckReport()
    simulation_check_report.performance_check_report = PerformanceCheckReport(
        valid_show_simulation.frames
    )
    apply_performance_check_procedure(
        valid_show_simulation,
        simulation_check_report.performance_check_report,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
    )
    assert simulation_check_report.performance_check_report.performance_slices_check_report[
        41
    ].horizontal_acceleration_check_report.validation


def test_invalid_up_force_simulation():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    distance_max = parameter.frame_parameter.position_fps * np.sqrt(
        parameter.iostar_parameter.force_up_max
        / parameter.iostar_parameter.iostar_drag_vertical_coef
    )
    position_event_1 = PositionEvent(
        6,
        0,
        0,
        distance_max,
    )
    position_event_2 = PositionEvent(
        12,
        0,
        0,
        2 * distance_max,
    )
    position_event_3 = PositionEvent(
        18,
        0,
        0,
        2 * distance_max + EPSILON_DELTA,
    )
    valid_show_simulation = get_show_simulation(
        [
            position_event_1,
            position_event_2,
            position_event_3,
        ]
    )
    simulation_check_report = SimulationCheckReport()
    simulation_check_report.performance_check_report = PerformanceCheckReport(
        valid_show_simulation.frames
    )
    apply_performance_check_procedure(
        valid_show_simulation,
        simulation_check_report.performance_check_report,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
    )
    assert not (
        simulation_check_report.performance_check_report.performance_slices_check_report[
            42
        ].up_force_check_report.validation
    )
