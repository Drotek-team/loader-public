from typing import List, Tuple

import numpy as np
import pytest

from ...drones_manager.drones_manager import Drone, DronesManager


def get_random_positions(nb_drones: int) -> List[Tuple[int, int, int]]:
    return [
        (
            int(np.random.normal(scale=10)),
            int(np.random.normal(scale=10)),
            int(np.random.normal(scale=10)),
        )
        for _ in range(nb_drones)
    ]


@pytest.fixture
def valid_drones_manager() -> DronesManager:
    nb_drones = 10
    drones = [Drone() for _ in range(nb_drones)]
    random_positions = get_random_positions(nb_drones)
    for random_position, drone in zip(random_positions, drones):
        drone.add_position(0, random_position)
    return DronesManager(drones)


### TO DO: add strategies to these tests
def test_valid_convex_hull(valid_drones_manager: DronesManager):
    assert True
