import numpy as np
import pytest

from ....drones_manager.drone.events.position_events import PositionEvent
from ....parameter.parameter import Parameter
from ....show_simulation.dance_simulation.convert_drone_to_dance_simulation import (
    flight_simulation,
)
from ....show_simulation.dance_simulation.position_simulation import (
    linear_interpolation,
)


def test_flight_simulation():
    parameter = Parameter()
    parameter.load_iostar_parameter()
    parameter.load_export_parameter()
    FIRST_POSITION_EVENT = PositionEvent(0, 0, 0, 0)
    SECOND_POSITION_EVENT = PositionEvent(250, 0, 0, 1_00)
    THIRD_POSITION_EVENT = PositionEvent(1000, 0, 0, 2_00)
    position_events = [
        FIRST_POSITION_EVENT,
        SECOND_POSITION_EVENT,
        THIRD_POSITION_EVENT,
    ]
    dance_sequence = flight_simulation(
        position_events,
        parameter.timecode_parameter,
        parameter.json_convertion_constant,
    )
    first_theorical_curve = linear_interpolation(
        FIRST_POSITION_EVENT.get_values(),
        SECOND_POSITION_EVENT.get_values(),
        (SECOND_POSITION_EVENT.timecode - FIRST_POSITION_EVENT.timecode)
        // parameter.timecode_parameter.position_timecode_rate,
        parameter.json_convertion_constant,
    )
    second_theorical_curve = linear_interpolation(
        SECOND_POSITION_EVENT.get_values(),
        THIRD_POSITION_EVENT.get_values(),
        (THIRD_POSITION_EVENT.timecode - SECOND_POSITION_EVENT.timecode)
        // parameter.timecode_parameter.position_timecode_rate,
        parameter.json_convertion_constant,
    )
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
