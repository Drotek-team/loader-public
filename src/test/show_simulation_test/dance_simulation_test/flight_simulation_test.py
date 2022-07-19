import numpy as np

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
    SECOND_POSITION_EVENT = PositionEvent(0.25, 0, 0, 1)
    THIRD_POSITION_EVENT = PositionEvent(1.0, 0, 0, 2)
    position_events = [
        FIRST_POSITION_EVENT,
        SECOND_POSITION_EVENT,
        THIRD_POSITION_EVENT,
    ]
    dance_sequence = flight_simulation(
        position_events,
        parameter.timecode_parameter,
    )
    first_theorical_curve = linear_interpolation(
        FIRST_POSITION_EVENT.get_values(),
        SECOND_POSITION_EVENT.get_values(),
        int(
            (SECOND_POSITION_EVENT.timecode - FIRST_POSITION_EVENT.timecode)
            / parameter.timecode_parameter.position_second_rate
        ),
    )
    second_theorical_curve = linear_interpolation(
        SECOND_POSITION_EVENT.get_values(),
        THIRD_POSITION_EVENT.get_values(),
        int(
            (THIRD_POSITION_EVENT.timecode - SECOND_POSITION_EVENT.timecode)
            / parameter.timecode_parameter.position_second_rate
        ),
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
