import os
from typing import ParamSpec

import pytest

from ....drones_user.drone.drone import DroneUser
from ....drones_user.drones_user import DronesUser
from ....family_user.family_user import FamilyUser
from ....parameter.parameter import Parameter
from .family_user_check_procedure import (
    apply_family_check_procedure,
)
from .family_user_check_report import (
    FamilyUserCheckReport,
)
import numpy as np


@pytest.fixture
def invalid_drones_user_inverse_first_positions():
    drone_1 = DroneUser(0)
    drone_1.add_position(0, (-100, 100, 0))
    drone_2 = DroneUser(1)
    drone_2.add_position(0, (100, -100, 0))
    drone_3 = DroneUser(2)
    drone_3.add_position(0, (100, 100, 0))
    drone_4 = DroneUser(3)
    drone_4.add_position(0, (-100, -100, 0))
    return DronesUser([drone_1, drone_2, drone_3, drone_4])


@pytest.fixture
def valid_family_user_angle():
    return FamilyUser(
        nb_x=2,
        nb_y=2,
        nb_drone_per_family=1,
        step_takeoff=200,
        angle_takeoff=45,
        show_duration_second=0,
        altitude_range_meter=[0, 10],
    )


@pytest.fixture
def invalid_family_user_drone_per_family():
    return FamilyUser(
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
    family_user_check_report = FamilyUserCheckReport()
    # Define drones_user
    drone_1 = DroneUser(0)
    drone_1.add_position(0, (-100, -100, 0))
    drone_2 = DroneUser(1)
    drone_2.add_position(0, (-100, 100, 0))
    drone_3 = DroneUser(2)
    drone_3.add_position(0, (100, -100, 0))
    drone_4 = DroneUser(3)
    drone_4.add_position(0, (100, 100, 0))
    valid_drones_user = DronesUser([drone_1, drone_2, drone_3, drone_4])
    # Define family_user
    valid_family_user = FamilyUser(
        nb_x=2,
        nb_y=2,
        nb_drone_per_family=1,
        step_takeoff=200,
        angle_takeoff=0,
        show_duration_second=valid_drones_user.duration
        * parameter.frame_parameter.json_fps,
        altitude_range_meter=valid_drones_user.altitude_range,
    )
    apply_family_check_procedure(
        valid_drones_user,
        valid_family_user,
        parameter.frame_parameter,
        parameter.json_convertion_constant,
        parameter.family_parameter,
        family_user_check_report,
    )
    assert family_user_check_report.validation


def test_valid_drones_user_family_angle():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    angle_radian = 45
    new_distance = np.sqrt(2)
    drone_1 = DroneUser(0)
    drone_1.add_position(0, (-int(new_distance * 100), 0, 0))
    drone_2 = DroneUser(1)
    drone_2.add_position(0, (0, int(new_distance * 100), 0))
    drone_3 = DroneUser(2)
    drone_3.add_position(0, (0, -int(new_distance * 100), 0))
    drone_4 = DroneUser(3)
    drone_4.add_position(
        0,
        (int(new_distance * 100), 0, 0),
    )
    valid_drones_user_angle = DronesUser([drone_1, drone_2, drone_3, drone_4])
    valid_family_user_angle = FamilyUser(
        nb_x=2,
        nb_y=2,
        nb_drone_per_family=1,
        step_takeoff=200,
        angle_takeoff=angle_radian,
        show_duration_second=valid_drones_user_angle.duration
        * parameter.frame_parameter.json_fps,
        altitude_range_meter=valid_drones_user_angle.altitude_range,
    )
    family_user_check_report = FamilyUserCheckReport()
    apply_family_check_procedure(
        valid_drones_user_angle,
        valid_family_user_angle,
        parameter.frame_parameter,
        parameter.json_convertion_constant,
        parameter.family_parameter,
        family_user_check_report,
    )
    assert family_user_check_report.validation


def test_invalid_drone_manager_first_positions():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())

    # Define drones_user
    drone_1 = DroneUser(0)
    drone_1.add_position(0, (-100, 100, 0))
    drone_2 = DroneUser(1)
    drone_2.add_position(0, (100, -100, 0))
    drone_3 = DroneUser(2)
    drone_3.add_position(0, (100, 100, 0))
    drone_4 = DroneUser(3)
    drone_4.add_position(0, (-100, -99, 0))
    invalid_first_position_drones_user = DronesUser(
        [drone_1, drone_2, drone_3, drone_4]
    )

    # Define family_user
    valid_family_user = FamilyUser(
        nb_x=2,
        nb_y=2,
        nb_drone_per_family=1,
        step_takeoff=200,
        angle_takeoff=0,
        show_duration_second=invalid_first_position_drones_user.duration
        * parameter.frame_parameter.json_fps,
        altitude_range_meter=invalid_first_position_drones_user.altitude_range,
    )
    family_user_check_report = FamilyUserCheckReport()
    apply_family_check_procedure(
        invalid_first_position_drones_user,
        valid_family_user,
        parameter.frame_parameter,
        parameter.json_convertion_constant,
        parameter.family_parameter,
        family_user_check_report,
    )
    assert not (family_user_check_report.family_user_logic_check_report.validation)
