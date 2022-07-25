import os

import numpy as np

from ....drones_manager.drone.events.position_events import PositionEvent
from ....parameter.parameter import Parameter
from ....show_simulation.dance_simulation.convert_trajectory_to_dance_simulation import (
    stand_by_simulation,
)
from ....show_simulation.dance_simulation.position_simulation import (
    linear_interpolation,
)


def test_stand_by_simulation():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    second_start = 0
    second_end = 1
    first_takeoff_position = (0, 0, 10)
    dance_sequence = stand_by_simulation(
        second_start,
        second_end,
        first_takeoff_position,
        parameter.timecode_parameter,
    )
    FIRST_THEORICAL_POSITION_EVENT = PositionEvent(
        second_start, *first_takeoff_position
    )
    SECOND_THEORICAL_POSITION_EVENT = PositionEvent(second_end, *first_takeoff_position)
    theorical_curve = linear_interpolation(
        FIRST_THEORICAL_POSITION_EVENT.get_values(),
        SECOND_THEORICAL_POSITION_EVENT.get_values(),
        int(
            (
                SECOND_THEORICAL_POSITION_EVENT.timecode
                - FIRST_THEORICAL_POSITION_EVENT.timecode
            )
            / parameter.timecode_parameter.position_second_rate
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
