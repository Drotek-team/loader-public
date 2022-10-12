from typing import List, Tuple
import numpy as np

### TO DO: adapt that to new format
def linear_interpolation(
    position_begin: Tuple[float, float, float],
    position_end: Tuple[float, float, float],
    nb_points: int,
    end_point: bool = False,
) -> List[np.ndarray]:
    if nb_points < 0:
        raise ValueError
    if nb_points == 0:
        return []
    return [
        np.round(
            np.array(position_begin) * (1 - percentile)
            + np.array(position_end) * percentile,
            2,
        )
        for percentile in np.linspace(
            0,
            1,
            nb_points,
            endpoint=end_point,
        )
    ]


VELOCITY_ESTIMATION_INDEX = 1
ACCELERATION_ESTIMATION_INDEX = 2


def get_velocity_acceleration_from_positions(
    positions: List[np.ndarray], position_fps: int
) -> Tuple[List[np.ndarray], List[np.ndarray]]:
    positions_array = np.array(positions)
    velocities_array = np.concatenate(
        (np.array([0]), position_fps * (positions_array[1:] - positions_array[:-1]))
    )
    accelerations_array = np.concatenate(
        (np.array([0]), position_fps * (velocities_array[1:] - velocities_array[:-1]))
    )
    return list(velocities_array), list(accelerations_array)
