import numpy as np
import pytest

from ....drones_manager.drone.events.position_events import PositionEvent
from ....parameter.parameter import Parameter
from ....show_simulation.dance_simulation.convert_drone_to_dance_simulation import (
    stand_by_simulation,
)
from ....show_simulation.dance_simulation.position_simulation import (
    linear_interpolation,
)


def test_stand_by_simulation():
    parameter = Parameter()
    parameter.load_iostar_parameter()
    parameter.load_export_parameter()
    timecode_start = 0
    timecode_end = 1_000
    first_takeoff_position = (0, 0, 10_00)
    dance_sequence = stand_by_simulation(
        timecode_start,
        timecode_end,
        first_takeoff_position,
        parameter.timecode_parameter,
        parameter.json_convention_constant,
    )
    FIRST_THEORICAL_POSITION_EVENT = PositionEvent(
        timecode_start, *first_takeoff_position
    )
    SECOND_THEORICAL_POSITION_EVENT = PositionEvent(
        timecode_end, *first_takeoff_position
    )
    theorical_curve = linear_interpolation(
        FIRST_THEORICAL_POSITION_EVENT.get_values(),
        SECOND_THEORICAL_POSITION_EVENT.get_values(),
        (
            SECOND_THEORICAL_POSITION_EVENT.timecode
            - FIRST_THEORICAL_POSITION_EVENT.timecode
        )
        // parameter.timecode_parameter.position_timecode_rate,
        parameter.json_convention_constant,
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
