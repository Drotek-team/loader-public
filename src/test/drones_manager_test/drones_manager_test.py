from typing import List, Tuple

import numpy as np
import pytest

from ...drones_manager.drones_manager import Drone, DronesManager


@pytest.fixture
def valid_drones_manager() -> DronesManager:
    nb_drones = 10
    drones = [Drone(drone_index) for drone_index in range(nb_drones)]
    random_positions = [
        (
            int(np.random.normal(scale=10)),
            int(np.random.normal(scale=10)),
            int(np.random.normal(scale=10)),
        )
        for _ in range(nb_drones)
    ]
    for random_position, drone in zip(random_positions, drones):
        drone.add_position(0, random_position)
    return DronesManager(drones)


### TO DO: add hypothesis/strategies to these tests
def test_valid_convex_hull(valid_drones_manager: DronesManager):
    assert True
