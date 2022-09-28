import os
from typing import ParamSpec

import pytest

from ....drones_manager.drone.drone import DroneExport
from ....drones_manager.drones_manager import DronesManager
from ....family_manager.family_manager import FamilyManager
from ....parameter.parameter import Parameter
from .family_manager_check_procedure import (
    apply_family_check_procedure,
)
from .family_manager_check_report import (
    FamilyManagerCheckReport,
)
import numpy as np


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


@pytest.fixture
def valid_family_manager_angle():
    return FamilyManager(
        nb_x=2,
        nb_y=2,
        nb_drone_per_family=1,
        step_takeoff=200,
        angle_takeoff=45,
        show_duration_second=0,
        altitude_range_meter=[0, 10],
    )


@pytest.fixture
def invalid_family_manager_drone_per_family():
    return FamilyManager(
        nb_x=2,
        nb_y=2,
        nb_drone_per_family=2,
        step_takeoff=200,
        angle_takeoff=0,
        show_duration_second=0,
        altitude_range_meter=[0, 10],
    )


def test_valid_drone_manager_family():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    family_manager_check_report = FamilyManagerCheckReport()
    # Define drones_manager
    drone_1 = DroneExport(0)
    drone_1.add_position(0, (-100, -100, 0))
    drone_2 = DroneExport(1)
    drone_2.add_position(0, (-100, 100, 0))
    drone_3 = DroneExport(2)
    drone_3.add_position(0, (100, -100, 0))
    drone_4 = DroneExport(3)
    drone_4.add_position(0, (100, 100, 0))
    valid_drones_manager = DronesManager([drone_1, drone_2, drone_3, drone_4])
    # Define family_manager
    valid_family_manager = FamilyManager(
        nb_x=2,
        nb_y=2,
        nb_drone_per_family=1,
        step_takeoff=200,
        angle_takeoff=0,
        show_duration_second=valid_drones_manager.duration
        * parameter.frame_parameter.json_fps,
        altitude_range_meter=valid_drones_manager.altitude_range,
    )
    apply_family_check_procedure(
        valid_drones_manager,
        valid_family_manager,
        parameter.frame_parameter,
        parameter.json_convertion_constant,
        parameter.family_parameter,
        family_manager_check_report,
    )
    assert family_manager_check_report.validation


def test_valid_drones_manager_family_angle():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    angle_radian = 45
    new_distance = np.sqrt(2)
    drone_1 = DroneExport(0)
    drone_1.add_position(0, (-int(new_distance * 100), 0, 0))
    drone_2 = DroneExport(1)
    drone_2.add_position(0, (0, int(new_distance * 100), 0))
    drone_3 = DroneExport(2)
    drone_3.add_position(0, (0, -int(new_distance * 100), 0))
    drone_4 = DroneExport(3)
    drone_4.add_position(
        0,
        (int(new_distance * 100), 0, 0),
    )
    valid_drones_manager_angle = DronesManager([drone_1, drone_2, drone_3, drone_4])
    valid_family_manager_angle = FamilyManager(
        nb_x=2,
        nb_y=2,
        nb_drone_per_family=1,
        step_takeoff=200,
        angle_takeoff=angle_radian,
        show_duration_second=valid_drones_manager_angle.duration
        * parameter.frame_parameter.json_fps,
        altitude_range_meter=valid_drones_manager_angle.altitude_range,
    )
    family_manager_check_report = FamilyManagerCheckReport()
    apply_family_check_procedure(
        valid_drones_manager_angle,
        valid_family_manager_angle,
        parameter.frame_parameter,
        parameter.json_convertion_constant,
        parameter.family_parameter,
        family_manager_check_report,
    )
    assert family_manager_check_report.validation


def test_invalid_drone_manager_first_positions():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())

    # Define drones_manager
    drone_1 = DroneExport(0)
    drone_1.add_position(0, (-100, 100, 0))
    drone_2 = DroneExport(1)
    drone_2.add_position(0, (100, -100, 0))
    drone_3 = DroneExport(2)
    drone_3.add_position(0, (100, 100, 0))
    drone_4 = DroneExport(3)
    drone_4.add_position(0, (-100, -99, 0))
    invalid_first_position_drones_manager = DronesManager(
        [drone_1, drone_2, drone_3, drone_4]
    )

    # Define family_manager
    valid_family_manager = FamilyManager(
        nb_x=2,
        nb_y=2,
        nb_drone_per_family=1,
        step_takeoff=200,
        angle_takeoff=0,
        show_duration_second=invalid_first_position_drones_manager.duration
        * parameter.frame_parameter.json_fps,
        altitude_range_meter=invalid_first_position_drones_manager.altitude_range,
    )
    family_manager_check_report = FamilyManagerCheckReport()
    apply_family_check_procedure(
        invalid_first_position_drones_manager,
        valid_family_manager,
        parameter.frame_parameter,
        parameter.json_convertion_constant,
        parameter.family_parameter,
        family_manager_check_report,
    )
    assert not (
        family_manager_check_report.family_manager_logic_check_report.validation
    )
