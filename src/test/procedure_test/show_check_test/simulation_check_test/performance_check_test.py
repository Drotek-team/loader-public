import os
from typing import List
import numpy as np
from .....drones_manager.drone.events.position_events import PositionEvent
from .....drones_manager.drones_manager import DroneExport, DronesManager
from .....parameter.parameter import Parameter
from .....procedure.show_check.simulation_check.performance_check.performance_check_procedure import (
    apply_performance_check_procedure,
)
from .....procedure.show_check.simulation_check.performance_check.performance_check_report import (
    PerformanceCheckReport,
)
from .....show_simulation.show_simulation import ShowSimulation, get_slices
from .....procedure.show_check.simulation_check.simulation_check_report import (
    SimulationCheckReport,
)


def get_show_simulation(position_events: List[PositionEvent]) -> ShowSimulation:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    drone = DroneExport(0)
    drone.add_position(0, (0, 0, 0))
    drone.add_position(
        parameter.takeoff_parameter.takeoff_duration,
        (0, 0, -parameter.takeoff_parameter.takeoff_altitude_meter),
    )
    for position_event in position_events:
        position = position_event.get_values()
        drone.add_position(
            parameter.takeoff_parameter.takeoff_duration + position_event.frame,
            (
                position[0],
                position[1],
                -parameter.takeoff_parameter.takeoff_altitude + position[2],
            ),
        )

    drones_manager = DronesManager([drone])
    show_simulation = ShowSimulation(
        get_slices(
            drones_manager.get_trajectory_simulation_manager(
                parameter.json_convertion_constant
            ),
            parameter.frame_parameter,
            parameter.takeoff_parameter,
            parameter.land_parameter,
        )
    )
    return show_simulation


def test_valid_simulation():
    position_event_1 = PositionEvent(250, 0, 0, 0)
    position_event_2 = PositionEvent(500, 0, 0, 0)
    position_event_3 = PositionEvent(750, 0, 0, 0)
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


def test_invalid_horizontal_velocity_simulation():
    ### The second position event is mandatory as it is the last position of the show so it is not a part of the dance (so the associate TO DO)
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    distance_max = (
        parameter.iostar_parameter.horizontal_velocity_max
        * parameter.frame_parameter.position_second_rate
    )
    position_event_1 = PositionEvent(
        250,
        int(
            distance_max * parameter.json_convertion_constant.METER_TO_CENTIMETER_RATIO
        ),
        0,
        0,
    )
    position_event_2 = PositionEvent(500, 1250_00, 0, 0)
    valid_show_simulation = get_show_simulation([position_event_1, position_event_2])
    simulation_check_report = SimulationCheckReport()
    simulation_check_report.performance_check_report = PerformanceCheckReport(
        valid_show_simulation.seconds
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
    ### The second position event is mandatory as it is the last position of the show so it is not a part of the dance (so the associate TO DO)
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    distance_max = (
        parameter.iostar_parameter.horizontal_velocity_max
        * parameter.frame_parameter.position_second_rate
    )
    position_event_1 = PositionEvent(
        250,
        int(distance_max * parameter.json_convertion_constant.METER_TO_CENTIMETER_RATIO)
        - 1,
        0,
        0,
    )
    position_event_2 = PositionEvent(500, 1250_00, 0, 0)
    valid_show_simulation = get_show_simulation([position_event_1, position_event_2])
    simulation_check_report = SimulationCheckReport()
    simulation_check_report.performance_check_report = PerformanceCheckReport(
        valid_show_simulation.seconds
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
    ### The second position event is mandatory as it is the last position of the show so it is not a part of the dance (so the associate TO DO)
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    distance_max = (
        parameter.iostar_parameter.horizontal_acceleration_max
        * parameter.frame_parameter.position_second_rate
        * parameter.frame_parameter.position_second_rate
    )
    position_event_1 = PositionEvent(
        250,
        int(distance_max * parameter.json_convertion_constant.METER_TO_CENTIMETER_RATIO)
        + 1,
        0,
        0,
    )
    position_event_2 = PositionEvent(500, 0, 0, 0)
    valid_show_simulation = get_show_simulation([position_event_1, position_event_2])
    simulation_check_report = SimulationCheckReport()
    simulation_check_report.performance_check_report = PerformanceCheckReport(
        valid_show_simulation.seconds
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
    ### The second position event is mandatory as it is the last position of the show so it is not a part of the dance (so the associate TO DO)
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    distance_max = (
        parameter.iostar_parameter.horizontal_acceleration_max
        * parameter.frame_parameter.position_second_rate
        * parameter.frame_parameter.position_second_rate
    )
    position_event_1 = PositionEvent(
        250,
        int(
            distance_max * parameter.json_convertion_constant.METER_TO_CENTIMETER_RATIO
        ),
        0,
        0,
    )
    position_event_2 = PositionEvent(500, 0, 0, 0)
    valid_show_simulation = get_show_simulation([position_event_1, position_event_2])
    simulation_check_report = SimulationCheckReport()
    simulation_check_report.performance_check_report = PerformanceCheckReport(
        valid_show_simulation.seconds
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
    distance_max = parameter.frame_parameter.position_second_rate * np.sqrt(
        parameter.iostar_parameter.force_up_max
        / parameter.iostar_parameter.iostar_drag_vertical_coef
    )
    position_event_1 = PositionEvent(
        250,
        0,
        0,
        -distance_max * parameter.json_convertion_constant.METER_TO_CENTIMETER_RATIO,
    )
    position_event_2 = PositionEvent(
        500,
        0,
        0,
        -2
        * (distance_max * parameter.json_convertion_constant.METER_TO_CENTIMETER_RATIO),
    )
    position_event_3 = PositionEvent(
        750,
        0,
        0,
        -2
        * (
            distance_max * parameter.json_convertion_constant.METER_TO_CENTIMETER_RATIO
            + 1
        ),
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
        valid_show_simulation.seconds
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


def test_invalid_up_force_limitation_simulation():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    distance_max = parameter.frame_parameter.position_second_rate * np.sqrt(
        parameter.iostar_parameter.force_up_max
        / parameter.iostar_parameter.iostar_drag_vertical_coef
    )
    position_event_1 = PositionEvent(
        250,
        0,
        0,
        -distance_max * parameter.json_convertion_constant.METER_TO_CENTIMETER_RATIO
        + 1,
    )
    position_event_2 = PositionEvent(
        500,
        0,
        0,
        -2
        * (distance_max * parameter.json_convertion_constant.METER_TO_CENTIMETER_RATIO)
        + 2,
    )
    position_event_3 = PositionEvent(
        750,
        0,
        0,
        -2
        * (
            distance_max * parameter.json_convertion_constant.METER_TO_CENTIMETER_RATIO
            + 1
        ),
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
        valid_show_simulation.seconds
    )
    apply_performance_check_procedure(
        valid_show_simulation,
        simulation_check_report.performance_check_report,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
    )
    assert simulation_check_report.performance_check_report.performance_slices_check_report[
        42
    ].up_force_check_report.validation
