import os

import numpy as np

from .....parameter.parameter import Parameter
from ..flight_simulation import linear_interpolation, flight_simulation
from .....show_dev.show_dev import PositionEventDev


def test_flight_simulation():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    FIRST_POSITION_EVENT = PositionEventDev(0, (0, 0, 0))
    SECOND_POSITION_EVENT = PositionEventDev(6, (0, 0, 100))
    THIRD_POSITION_EVENT = PositionEventDev(24, (0, 0, 200))
    position_events = [
        FIRST_POSITION_EVENT,
        SECOND_POSITION_EVENT,
        THIRD_POSITION_EVENT,
    ]
    dance_sequence = flight_simulation(
        position_events,
        parameter.frame_parameter,
    )
    first_theorical_curve = linear_interpolation(
        FIRST_POSITION_EVENT.xyz,
        SECOND_POSITION_EVENT.xyz,
        int(
            (SECOND_POSITION_EVENT.frame - FIRST_POSITION_EVENT.frame)
            // parameter.frame_parameter.position_rate_frame
        ),
    )
    second_theorical_curve = linear_interpolation(
        SECOND_POSITION_EVENT.xyz,
        THIRD_POSITION_EVENT.xyz,
        int(
            (THIRD_POSITION_EVENT.frame - SECOND_POSITION_EVENT.frame)
            // parameter.frame_parameter.position_rate_frame
        ),
    ) + [np.array(THIRD_POSITION_EVENT.xyz)]
    theorical_curve = first_theorical_curve + second_theorical_curve
    assert len(dance_sequence.drone_positions) == len(theorical_curve)
    assert all(
        [
            np.array_equal(drone_position, theorical_position)
            for drone_position, theorical_position in zip(
                dance_sequence.drone_positions, theorical_curve
            )
        ]
    )
    assert all(dance_sequence.drone_in_air) == True
    assert all(dance_sequence.drone_in_dance) == True
