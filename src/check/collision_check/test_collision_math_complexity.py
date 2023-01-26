import time

import numpy as np

from .collision_math import get_couple_distance_matrix

ITERATION_NUMBER = 20 * 60 * 4  # 20 minutes, 60 seconds, 24 fps
DRONE_NUMBER = 200
ACTIVE = False


def test_get_couple_distance_matrix_complexity():
    if not ACTIVE:
        return
    positions = np.random.rand(DRONE_NUMBER, 3)
    time_begin = time.time()
    for _ in range(ITERATION_NUMBER):
        get_couple_distance_matrix(positions)
    raise ValueError(time.time() - time_begin)
