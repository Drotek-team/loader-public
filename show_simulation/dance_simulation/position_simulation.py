from typing import List

import numpy as np


class PositionSimulation:
    @staticmethod
    def linear_interpolation(
        point_begin: np.ndarray, point_end: np.ndarray, nb_points: int
    ) -> List[np.ndarray]:
        return [
            point_begin * (frame_pct) + point_end * (1 - frame_pct)
            for frame_pct in np.linspace(
                0,
                1,
                nb_points,
            )
        ]

    @staticmethod
    def truncated_integer(integer: int, modulo) -> int:
        return (integer // modulo + 1) * modulo
