from typing import List, Tuple

import numpy as np

from ...parameter.parameter import JsonConventionConstant


def linear_interpolation(
    position_begin: Tuple[int, int, int],
    position_end: Tuple[int, int, int],
    nb_points: int,
    json_convention_constant: JsonConventionConstant,
) -> List[np.ndarray]:
    if nb_points == 0:
        return []
    position_begin_simulation = (
        json_convention_constant.from_json_position_to_simulation_position(
            position_begin
        )
    )
    position_end_simulation = (
        json_convention_constant.from_json_position_to_simulation_position(position_end)
    )
    return [
        np.round(
            position_begin_simulation * (1 - percentile)
            + position_end_simulation * percentile,
            2,
        )
        for percentile in np.linspace(
            0,
            1,
            nb_points,
            endpoint=False,
        )
    ]
