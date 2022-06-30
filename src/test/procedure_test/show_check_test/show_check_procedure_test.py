from typing import Tuple

import pytest

from ....drones_manager.drones_manager import Drone, DronesManager
from ....family_manager.family_manager import FamilyManager
from ....parameter.parameter import Parameter


@pytest.fixture
def valid_drones_manager_family_manager() -> Tuple(DronesManager, FamilyManager):
    parameter = Parameter()
    parameter.load_parameter()
    drone = Drone()
    drone.add_position(0, (0, 0, 0))
    drone.add_position(0, (0, 0, 0))
    drone.add_position(0, (0, 0, 0))


def test_valid_show_check_procedure():
    pass
