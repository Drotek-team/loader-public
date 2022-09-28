from curses.ascii import alt
import os
from typing import Tuple

import pytest

from ...drones_manager.drones_manager import DroneExport, DronesManager
from ...family_manager.family_manager import FamilyManager
from ...parameter.parameter import Parameter
from .show_check_procedure import apply_show_check_procedure
from .show_check_report import ShowCheckReport


@pytest.fixture
def valid_drones_manager_family_manager() -> Tuple[DronesManager, FamilyManager]:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    drone = DroneExport(0)
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
    drone_manager = DronesManager([drone])
    family_manager = FamilyManager(
        nb_x=1,
        nb_y=1,
        nb_drone_per_family=1,
        step_takeoff=100,
        angle_takeoff=0,
        show_duration_second=drone_manager.duration,
        altitude_range_meter=drone_manager.altitude_range,
    )
    return drone_manager, family_manager


def test_valid_show_check_procedure(
    valid_drones_manager_family_manager: Tuple[DronesManager, FamilyManager]
):
    drones_manager, family_manager = valid_drones_manager_family_manager
    show_check_report = ShowCheckReport(len(drones_manager.drones))
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    apply_show_check_procedure(
        drones_manager, family_manager, show_check_report, parameter
    )
    assert show_check_report.validation
