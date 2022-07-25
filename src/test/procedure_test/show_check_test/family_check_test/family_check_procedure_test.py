import pytest

from .....drones_manager.drone.drone import Drone
from .....drones_manager.drones_manager import DronesManager
from .....family_manager.family_manager import FamilyManager
from .....parameter.parameter import Parameter
from .....procedure.show_check.family_manager_check.family_manager_check_procedure import (
    apply_family_check_procedure,
)
from .....procedure.show_check.family_manager_check.family_manager_check_report import (
    FamilyManagerCheckReport,
)


@pytest.fixture
def valid_family_manager():
    return FamilyManager(
        nb_x=2, nb_y=2, nb_drone_per_family=1, step_takeoff=200, angle_takeoff=0
    )


@pytest.fixture
def valid_drones_manager():
    drone_1 = Drone(0)
    drone_1.add_position(0, (-100, -100, 0))
    drone_2 = Drone(1)
    drone_2.add_position(0, (-100, 100, 0))
    drone_3 = Drone(2)
    drone_3.add_position(0, (100, -100, 0))
    drone_4 = Drone(3)
    drone_4.add_position(0, (100, 100, 0))
    return DronesManager([drone_1, drone_2, drone_3, drone_4])


def test_valid_drone_manager_family_manager(
    valid_drones_manager: DronesManager, valid_family_manager: FamilyManager
):
    parameter = Parameter()
    parameter.load_parameter()
    family_manager_check_report = FamilyManagerCheckReport()
    apply_family_check_procedure(
        valid_drones_manager,
        valid_family_manager,
        parameter.family_parameter,
        family_manager_check_report,
    )
    assert family_manager_check_report.validation
