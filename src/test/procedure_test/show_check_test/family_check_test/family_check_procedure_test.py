import os

import pytest

from .....drones_manager.drone.drone import DroneExport
from .....drones_manager.drones_manager import DronesManager
from .....family_manager.family_manager import FamilyManager
from .....parameter.parameter import Parameter
from .....procedure.show_check.family_manager_check.family_manager_check_procedure import (
    apply_family_check_procedure,
)
from .....procedure.show_check.family_manager_check.family_manager_check_report import (
    FamilyManagerCheckReport,
)
import numpy as np


@pytest.fixture
def valid_family_manager():
    return FamilyManager(
        nb_x=2, nb_y=2, nb_drone_per_family=1, step_takeoff=200, angle_takeoff=0
    )


@pytest.fixture
def valid_family_manager_angle():
    return FamilyManager(
        nb_x=2, nb_y=2, nb_drone_per_family=1, step_takeoff=200, angle_takeoff=45
    )


@pytest.fixture
def invalid_family_manager_drone_per_family():
    return FamilyManager(
        nb_x=2, nb_y=2, nb_drone_per_family=2, step_takeoff=200, angle_takeoff=0
    )


@pytest.fixture
def valid_drones_manager():
    drone_1 = DroneExport(0)
    drone_1.add_position(0, (-100, -100, 0))
    drone_2 = DroneExport(1)
    drone_2.add_position(0, (-100, 100, 0))
    drone_3 = DroneExport(2)
    drone_3.add_position(0, (100, -100, 0))
    drone_4 = DroneExport(3)
    drone_4.add_position(0, (100, 100, 0))
    return DronesManager([drone_1, drone_2, drone_3, drone_4])


@pytest.fixture
def valid_drones_manager_angle():
    angle_factor = np.sqrt(2)
    drone_1 = DroneExport(0)
    drone_1.add_position(0, (-int(angle_factor * 100), 0, 0))
    drone_2 = DroneExport(1)
    drone_2.add_position(0, (0, int(angle_factor * 100), 0))
    drone_3 = DroneExport(2)
    drone_3.add_position(0, (0, -int(angle_factor * 100), 0))
    drone_4 = DroneExport(3)
    drone_4.add_position(0, (int(angle_factor * 100), 0, 0))
    return DronesManager([drone_1, drone_2, drone_3, drone_4])


@pytest.fixture
def invalid_drones_manager_first_positions():
    drone_1 = DroneExport(0)
    drone_1.add_position(0, (-100, 100, 0))
    drone_2 = DroneExport(1)
    drone_2.add_position(0, (100, -100, 0))
    drone_3 = DroneExport(2)
    drone_3.add_position(0, (100, 100, 0))
    drone_4 = DroneExport(3)
    drone_4.add_position(0, (-100, -99, 0))
    return DronesManager([drone_1, drone_2, drone_3, drone_4])


@pytest.fixture
def invalid_drones_manager_inverse_first_positions():
    drone_1 = DroneExport(0)
    drone_1.add_position(0, (-100, 100, 0))
    drone_2 = DroneExport(1)
    drone_2.add_position(0, (100, -100, 0))
    drone_3 = DroneExport(2)
    drone_3.add_position(0, (100, 100, 0))
    drone_4 = DroneExport(3)
    drone_4.add_position(0, (-100, -100, 0))
    return DronesManager([drone_1, drone_2, drone_3, drone_4])


def test_valid_drone_manager_family(
    valid_drones_manager: DronesManager, valid_family_manager: FamilyManager
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    family_manager_check_report = FamilyManagerCheckReport()
    apply_family_check_procedure(
        valid_drones_manager,
        valid_family_manager,
        parameter.family_parameter,
        family_manager_check_report,
    )
    assert family_manager_check_report.validation


def test_valid_drone_manager_family_angle(
    valid_drones_manager_angle: DronesManager, valid_family_manager_angle: FamilyManager
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    family_manager_check_report = FamilyManagerCheckReport()
    apply_family_check_procedure(
        valid_drones_manager_angle,
        valid_family_manager_angle,
        parameter.family_parameter,
        family_manager_check_report,
    )
    assert family_manager_check_report.validation


def test_invalid_drone_manager_first_positions(
    invalid_drones_manager_first_positions: DronesManager,
    valid_family_manager: FamilyManager,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    family_manager_check_report = FamilyManagerCheckReport()
    apply_family_check_procedure(
        invalid_drones_manager_first_positions,
        valid_family_manager,
        parameter.family_parameter,
        family_manager_check_report,
    )
    assert not (
        family_manager_check_report.coherence_check_report.position_coherence_check_report.validation
    )


def test_invalid_drone_manager_inverse_first_positions(
    invalid_drones_manager_inverse_first_positions: DronesManager,
    valid_family_manager: FamilyManager,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    family_manager_check_report = FamilyManagerCheckReport()
    apply_family_check_procedure(
        invalid_drones_manager_inverse_first_positions,
        valid_family_manager,
        parameter.family_parameter,
        family_manager_check_report,
    )
    assert not (
        family_manager_check_report.coherence_check_report.position_coherence_check_report.validation
    )


def test_invalid_family_manager_drone_per_family(
    valid_drones_manager: DronesManager,
    invalid_family_manager_drone_per_family: FamilyManager,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    family_manager_check_report = FamilyManagerCheckReport()
    apply_family_check_procedure(
        valid_drones_manager,
        invalid_family_manager_drone_per_family,
        parameter.family_parameter,
        family_manager_check_report,
    )
    assert not (
        family_manager_check_report.coherence_check_report.nb_drone_coherence_check_report.validation
    )
