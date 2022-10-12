import os

import numpy as np

from ....parameter.parameter import Parameter
from ..flight_simulation import linear_interpolation
from ..stand_by_simulation import stand_by_simulation
from ....show_dev.show_dev import PositionEventDev

FRAME_START = 0
FRAME_END = 20
POSITION = (0.0, 0.0, 10.0)


def test_stand_by_simulation():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    dance_sequence = stand_by_simulation(
        FRAME_START,
        FRAME_END,
        POSITION,
        parameter.frame_parameter,
    )
    FIRST_THEORICAL_POSITION_EVENT = PositionEventDev(FRAME_START, POSITION)
    SECOND_THEORICAL_POSITION_EVENT = PositionEventDev(FRAME_END, POSITION)
    theorical_curve = linear_interpolation(
        FIRST_THEORICAL_POSITION_EVENT.xyz,
        SECOND_THEORICAL_POSITION_EVENT.xyz,
        (
            int(
                (
                    SECOND_THEORICAL_POSITION_EVENT.frame
                    - FIRST_THEORICAL_POSITION_EVENT.frame
                )
                // parameter.frame_parameter.position_rate_frame
            )
        ),
    )
    assert len(dance_sequence.drone_positions) == len(theorical_curve)
    assert all(
        [
            np.array_equal(drone_position, theorical_position)
            for drone_position, theorical_position in zip(
                dance_sequence.drone_positions, theorical_curve
            )
        ]
    )
    assert all(dance_sequence.drone_in_air) == False
    assert all(dance_sequence.drone_in_dance) == False
