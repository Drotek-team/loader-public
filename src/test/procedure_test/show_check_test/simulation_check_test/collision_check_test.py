import os

import pytest

from src.procedure.show_check.simulation_check.collision_check.collision_check_report import (
    CollisionCheckReport,
)

from .....drones_manager.drones_manager import DroneExport, DronesManager
from .....parameter.parameter import Parameter
from .....procedure.show_check.simulation_check.collision_check.collision_check_procedure import (
    apply_collision_check_procedure,
)
from .....procedure.show_check.simulation_check.simulation_check_report import (
    SimulationCheckReport,
)
from .....show_simulation.show_simulation import ShowSimulation, get_slices


@pytest.fixture
def valid_show_simulation():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    first_drone, second_drone = DroneExport(0), DroneExport(1)
    first_drone.add_position(0, (0, 0, 0))
    first_drone.add_position(
        parameter.takeoff_parameter.takeoff_duration,
        (0, 0, -parameter.takeoff_parameter.takeoff_altitude),
    )
    second_drone.add_position(
        0,
        (
            parameter.json_convertion_constant.METER_TO_CENTIMETER_RATIO
            * parameter.iostar_parameter.security_distance_in_air,
            0,
            0,
        ),
    )
    second_drone.add_position(
        parameter.takeoff_parameter.takeoff_duration,
        (
            parameter.json_convertion_constant.METER_TO_CENTIMETER_RATIO
            * parameter.iostar_parameter.security_distance_in_air,
            0,
            -parameter.takeoff_parameter.takeoff_altitude,
        ),
    )
    drones_manager = DronesManager([first_drone, second_drone])
    show_simulation = ShowSimulation(
        get_slices(
            drones_manager.get_trajectory_simulation_manager(
                parameter.json_convertion_constant
            ),
            parameter.timecode_parameter,
            parameter.takeoff_parameter,
            parameter.land_parameter,
        )
    )
    return show_simulation


@pytest.fixture
def invalid_show_simulation():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    first_drone, second_drone = DroneExport(0), DroneExport(1)
    first_drone.add_position(0, (0, 0, 0))
    first_drone.add_position(
        parameter.takeoff_parameter.takeoff_duration,
        (0, 0, -parameter.takeoff_parameter.takeoff_altitude),
    )
    second_drone.add_position(
        0,
        (
            0.99
            * parameter.json_convertion_constant.METER_TO_CENTIMETER_RATIO
            * parameter.iostar_parameter.security_distance_in_air,
            0,
            0,
        ),
    )
    second_drone.add_position(
        parameter.takeoff_parameter.takeoff_duration,
        (
            0.99
            * parameter.json_convertion_constant.METER_TO_CENTIMETER_RATIO
            * parameter.iostar_parameter.security_distance_in_air,
            0,
            -parameter.takeoff_parameter.takeoff_altitude,
        ),
    )
    drones_manager = DronesManager([first_drone, second_drone])
    show_simulation = ShowSimulation(
        get_slices(
            drones_manager.get_trajectory_simulation_manager(
                parameter.json_convertion_constant
            ),
            parameter.timecode_parameter,
            parameter.takeoff_parameter,
            parameter.land_parameter,
        )
    )
    return show_simulation


def test_valid_simulation(valid_show_simulation: ShowSimulation):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    simulation_check_report = SimulationCheckReport()
    simulation_check_report.collision_check_report = CollisionCheckReport(
        valid_show_simulation.seconds
    )
    apply_collision_check_procedure(
        valid_show_simulation,
        simulation_check_report.collision_check_report,
        parameter.iostar_parameter,
    )
    assert simulation_check_report.collision_check_report.validation


def test_invalid_simulation(invalid_show_simulation: ShowSimulation):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    simulation_check_report = SimulationCheckReport()
    simulation_check_report.collision_check_report = CollisionCheckReport(
        invalid_show_simulation.seconds
    )
    apply_collision_check_procedure(
        invalid_show_simulation,
        simulation_check_report.collision_check_report,
        parameter.iostar_parameter,
    )
    assert not (simulation_check_report.collision_check_report.validation)
