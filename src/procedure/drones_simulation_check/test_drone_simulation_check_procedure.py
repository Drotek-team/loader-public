from ...show_simulation.drone_simulation import DroneSimulation, PositionEventSimulation
from .drone_simulation_check_report import (
    DroneSimulationCheckReport,
)
from ...parameter.parameter import Parameter
import os
import pytest
from .drone_simulation_check_procedure import apply_drone_simulation_check_procedure


@pytest.fixture
def valid_drone_simulation() -> DroneSimulation:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    return DroneSimulation(
        0,
        [
            PositionEventSimulation(0, (0.0, 0.0, 0.0)),
            PositionEventSimulation(
                int(
                    parameter.frame_parameter.json_fps
                    * parameter.takeoff_parameter.takeoff_duration_second
                ),
                (0.0, 0.0, parameter.takeoff_parameter.takeoff_altitude_meter),
            ),
        ],
    )


def test_valid_position_events_takeoff_duration_xyz_check(
    valid_drone_simulation: DroneSimulation,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    drone_simulation_check_report = DroneSimulationCheckReport(0)
    apply_drone_simulation_check_procedure(
        valid_drone_simulation,
        drone_simulation_check_report,
        parameter.takeoff_parameter,
        parameter.frame_parameter,
    )
    assert drone_simulation_check_report.takeoff_check_report.validation


@pytest.fixture
def invalid_drone_simulation_takeoff_duration() -> DroneSimulation:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    FRAME_BIAS = 1
    return DroneSimulation(
        0,
        [
            PositionEventSimulation(0, (0.0, 0.0, 0.0)),
            PositionEventSimulation(
                int(
                    parameter.frame_parameter.json_fps
                    * parameter.takeoff_parameter.takeoff_duration_second
                )
                + FRAME_BIAS,
                (0.0, 0.0, parameter.takeoff_parameter.takeoff_altitude_meter),
            ),
        ],
    )


def test_invalid_position_events_takeoff_duration_check(
    invalid_drone_simulation_takeoff_duration: DroneSimulation,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    drone_simulation_check_report = DroneSimulationCheckReport(0)
    apply_drone_simulation_check_procedure(
        invalid_drone_simulation_takeoff_duration,
        drone_simulation_check_report,
        parameter.takeoff_parameter,
        parameter.frame_parameter,
    )
    assert not (
        drone_simulation_check_report.takeoff_check_report.takeoff_duration_check_report.validation
    )
    assert (
        drone_simulation_check_report.takeoff_check_report.takeoff_xyz_check_report.validation
    )


@pytest.fixture
def invalid_drone_simulation_takeoff_xyz() -> DroneSimulation:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    Z_BIAS = 1e-2
    return DroneSimulation(
        0,
        [
            PositionEventSimulation(0, (0.0, 0.0, 0.0)),
            PositionEventSimulation(
                int(
                    parameter.frame_parameter.json_fps
                    * parameter.takeoff_parameter.takeoff_duration_second
                ),
                (0.0, 0.0, parameter.takeoff_parameter.takeoff_altitude_meter + Z_BIAS),
            ),
        ],
    )


def test_invalid_position_events_takeoff_xyz_check(
    invalid_drone_simulation_takeoff_xyz: DroneSimulation,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    drone_simulation_check_report = DroneSimulationCheckReport(0)
    apply_drone_simulation_check_procedure(
        invalid_drone_simulation_takeoff_xyz,
        drone_simulation_check_report,
        parameter.takeoff_parameter,
        parameter.frame_parameter,
    )
    assert (
        drone_simulation_check_report.takeoff_check_report.takeoff_duration_check_report.validation
    )
    assert not (
        drone_simulation_check_report.takeoff_check_report.takeoff_xyz_check_report.validation
    )