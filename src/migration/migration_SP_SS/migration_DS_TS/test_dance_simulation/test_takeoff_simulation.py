import os

import numpy as np

from .....parameter.parameter import Parameter
from ..flight_simulation import linear_interpolation
from ..takeoff_simulation import takeoff_simulation


def test_takeoff_simulation():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    first_position = (2.35, 5.36, 0.0)
    dance_sequence = takeoff_simulation(
        first_position,
        parameter.frame_parameter,
        parameter.takeoff_parameter,
    )
    LAST_THEORICAL_POSITION = (
        first_position[0],
        first_position[1],
        parameter.takeoff_parameter.takeoff_altitude_meter,
    )
    first_theorical_curve = linear_interpolation(
        first_position,
        LAST_THEORICAL_POSITION,
        int(
            parameter.takeoff_parameter.takeoff_elevation_duration_second
            * parameter.frame_parameter.position_fps
        ),
    )
    second_theorical_curve = linear_interpolation(
        LAST_THEORICAL_POSITION,
        LAST_THEORICAL_POSITION,
        int(
            parameter.takeoff_parameter.takeoff_stabilisation_duration_second
            * parameter.frame_parameter.position_fps
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
    assert dance_sequence.drone_in_air[0] == False
    assert all(dance_sequence.drone_in_air[1:]) == True
    assert all(dance_sequence.drone_in_dance) == False
