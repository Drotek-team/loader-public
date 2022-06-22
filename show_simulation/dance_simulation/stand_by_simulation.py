from typing import List, Tuple

import numpy as np


def stand_by_simulation(
    first_timecode: int,
    last_timecode: int,
    stand_by_position: np.ndarray,
    position_time_frequence: int,
) -> Tuple[List[np.ndarray], List[bool], List[bool]]:
    nb_element = (last_timecode - first_timecode) // position_time_frequence
    return (
        nb_element * [stand_by_position],
        nb_element * [False],
        nb_element * [False],
    )
