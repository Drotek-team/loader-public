from curses.ascii import alt
import os
from typing import Tuple

import pytest

from ...drones_user.drones_user import DroneUser, DronesUser
from ...family_user.family_user import FamilyUser
from ...parameter.parameter import Parameter
from .show_check_procedure import apply_show_check_procedure
from .show_check_report import ShowCheckReport


@pytest.fixture
def valid_drones_user_family_user() -> Tuple[DronesUser, FamilyUser]:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    drone = DroneUser(0)
    drone.add_position(0, (0, 0, 0))
    drone.add_position(
        int(
            parameter.frame_parameter.json_fps
            * parameter.takeoff_parameter.takeoff_duration_second
        ),
        (
            0,
            0,
            -int(
                parameter.json_convertion_constant.METER_TO_CENTIMETER_RATIO
                * parameter.takeoff_parameter.takeoff_altitude_meter
            ),
        ),
    )
    drone.add_position(
        int(
            parameter.frame_parameter.json_fps
            * parameter.takeoff_parameter.takeoff_duration_second
        )
        + 6,
        (
            0,
            0,
            -int(
                parameter.json_convertion_constant.METER_TO_CENTIMETER_RATIO
                * parameter.takeoff_parameter.takeoff_altitude_meter
            ),
        ),
    )
    drone_manager = DronesUser([drone])
    family_user = FamilyUser(
        nb_x=1,
        nb_y=1,
        nb_drone_per_family=1,
        step_takeoff=100,
        angle_takeoff=0,
        show_duration_second=drone_manager.duration,
        altitude_range_meter=drone_manager.altitude_range,
    )
    return drone_manager, family_user


def test_valid_show_check_procedure(
    valid_drones_user_family_user: Tuple[DronesUser, FamilyUser]
):
    drones_user, family_user = valid_drones_user_family_user
    show_check_report = ShowCheckReport(len(drones_user.drones))
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    apply_show_check_procedure(drones_user, family_user, show_check_report, parameter)
    assert show_check_report.validation
