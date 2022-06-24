import pytest

from .....drones_manager.drone.drone import Drone
from .....drones_manager.drones_manager import DronesManager
from .....family_manager.family_manager import FamilyManager
from .....procedure.show_check.family_manager_check.family_manager_check_procedure import (
    apply_family_check_procedure,
)
from .....procedure.show_check.family_manager_check.family_manager_check_report import (
    FamilyManagerCheckReport,
)


@pytest.fixture
def valid_family_manager():
    family_manager = FamilyManager()
    family_manager.nb_x = 2
    family_manager.nb_y = 2
    family_manager.step = 2
    family_manager.angle = 0
    return family_manager


@pytest.fixture
def valid_drones_manager():
    drones_manager = DronesManager()
    drone_1 = Drone()
    drone_1.add_position(0, (100, 100, 0))
    drones_manager.drones.append(drone_1)
    drone_2 = Drone()
    drone_2.add_position(0, (100, -100, 0))
    drones_manager.drones.append(drone_2)
    drone_3 = Drone()
    drone_3.add_position(0, (-100, 100, 0))
    drones_manager.drones.append(drone_3)
    drone_4 = Drone()
    drone_4.add_position(0, (-100, -100, 0))
    drones_manager.drones.append(drone_4)
    return drones_manager


def test_valid_family_manager(
    valid_drones_manager: DronesManager, valid_family_manager: FamilyManager
):
    family_manager_check_report = FamilyManagerCheckReport
    apply_family_check_procedure(
        valid_drones_manager, valid_family_manager, family_manager_check_report
    )
