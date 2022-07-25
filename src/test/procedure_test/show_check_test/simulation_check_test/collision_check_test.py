import numpy as np
import pytest

from .....drones_manager.drones_manager import Drone, DronesManager
from .....parameter.parameter import Parameter
from .....procedure.show_check.simulation_check.collision_check.collision_check_procedure import (
    apply_collision_check_procedure,
)
from .....procedure.show_check.simulation_check.collision_check.collision_check_report import (
    CollisionCheckReport,
)
from .....show_simulation.show_simulation import ShowSimulation


@pytest.fixture
def valid_show_simulation():
    parameter = Parameter()
    parameter.load_parameter()
    first_drone, second_drone = Drone(0), Drone(1)
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
    trajectory_simulation_manager = drones_manager.get_trajectory_simulation_manager(
        parameter.json_convertion_constant
    )
    show_simulation = ShowSimulation(
        len(trajectory_simulation_manager.trajectories_simulation),
        trajectory_simulation_manager.get_last_second(parameter.land_parameter),
    )
    show_simulation.update_show_slices(
        parameter.timecode_parameter,
    )
    for trajectory_simulation in trajectory_simulation_manager.trajectories_simulation:
        show_simulation.add_dance_simulation(
            trajectory_simulation,
            parameter.timecode_parameter,
            parameter.takeoff_parameter,
            parameter.land_parameter,
        )
    return show_simulation


@pytest.fixture
def invalid_show_simulation():
    parameter = Parameter()
    parameter.load_parameter()
    first_drone, second_drone = Drone(0), Drone(1)
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
    trajectory_simulation_manager = drones_manager.get_trajectory_simulation_manager(
        parameter.json_convertion_constant
    )
    show_simulation = ShowSimulation(
        len(trajectory_simulation_manager.trajectories_simulation),
        trajectory_simulation_manager.get_last_second(parameter.land_parameter),
    )
    show_simulation.update_show_slices(
        parameter.timecode_parameter,
    )
    for trajectory_simulation in trajectory_simulation_manager.trajectories_simulation:
        show_simulation.add_dance_simulation(
            trajectory_simulation,
            parameter.timecode_parameter,
            parameter.takeoff_parameter,
            parameter.land_parameter,
        )
    return show_simulation


def test_valid_simulation(valid_show_simulation: ShowSimulation):
    parameter = Parameter()
    parameter.load_parameter()
    collision_check_report = CollisionCheckReport()
    apply_collision_check_procedure(
        valid_show_simulation, collision_check_report, parameter.iostar_parameter
    )
    assert collision_check_report.validation


def test_invalid_simulation(invalid_show_simulation: ShowSimulation):
    parameter = Parameter()
    parameter.load_parameter()
    collision_check_report = CollisionCheckReport()
    apply_collision_check_procedure(
        invalid_show_simulation, collision_check_report, parameter.iostar_parameter
    )
    assert not (collision_check_report.validation)
