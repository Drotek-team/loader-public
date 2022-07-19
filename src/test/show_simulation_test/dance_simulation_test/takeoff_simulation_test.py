import numpy as np
import pytest

from ....parameter.parameter import Parameter
from ....show_simulation.dance_simulation.convert_drone_to_dance_simulation import (
    takeoff_simulation,
)
from ....show_simulation.dance_simulation.position_simulation import (
    linear_interpolation,
)


def test_takeoff_simulation():
    parameter = Parameter()
    parameter.load_iostar_parameter()
    parameter.load_export_parameter()
    first_position = (2.35, 5.36, 0.0)
    dance_sequence = takeoff_simulation(
        first_position,
        parameter.timecode_parameter,
        parameter.takeoff_parameter,
    )
    LAST_THEORICAL_POSITION = (
        first_position[0],
        first_position[1],
        parameter.takeoff_parameter.takeoff_simulation_altitude,
    )
    first_theorical_curve = linear_interpolation(
        first_position,
        LAST_THEORICAL_POSITION,
        int(
            parameter.takeoff_parameter.takeoff_elevation_duration
            / parameter.timecode_parameter.position_timecode_rate,
        ),
    )
    second_theorical_curve = linear_interpolation(
        LAST_THEORICAL_POSITION,
        LAST_THEORICAL_POSITION,
        int(
            parameter.takeoff_parameter.takeoff_stabilisation_duration
            / parameter.timecode_parameter.position_timecode_rate
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
    assert all(dance_sequence.drone_in_dance) == False
