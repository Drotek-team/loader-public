import os

import numpy as np

from .....parameter.parameter import Parameter
from ..in_air_flight_simulation import linear_interpolation
from ...simulation.land_simulation import land_simulation


def test_land_simulation_first_case():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    X_METER = 2
    Y_METER = 2
    HGT_CENTIMETER = 1
    first_takeoff_position = (X_METER, Y_METER, HGT_CENTIMETER)

    dance_sequence = land_simulation(
        first_takeoff_position,
        parameter.frame_parameter,
        parameter.land_parameter,
    )
    THEORICAL_LAST_TAKEOFF_POSITION = (X_METER, Y_METER, 0)
    THEORICAL_NB_POINT = int(
        parameter.land_parameter.get_first_land_second_delta(HGT_CENTIMETER)
        // parameter.frame_parameter.position_rate_second
    )
    theorical_curve = linear_interpolation(
        first_takeoff_position,
        THEORICAL_LAST_TAKEOFF_POSITION,
        THEORICAL_NB_POINT,
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
    assert all(dance_sequence.drone_in_air) == True
    assert all(dance_sequence.drone_in_dance) == False


def test_land_simulation_second_case():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    X_METER = 2
    Y_METER = 2
    HGT_CENTIMETER = 5
    first_takeoff_position = (X_METER, Y_METER, HGT_CENTIMETER)
    dance_sequence = land_simulation(
        first_takeoff_position,
        parameter.frame_parameter,
        parameter.land_parameter,
    )
    THEORICAL_MIDDLE_TAKEOFF_POSITION = (
        X_METER,
        Y_METER,
        parameter.land_parameter.land_safe_hgt,
    )
    THEORICAL_END_TAKEOFF_POSITION = (
        X_METER,
        Y_METER,
        0,
    )
    FIRST_THEORICAL_NB_POINT = int(
        parameter.land_parameter.get_first_land_second_delta(HGT_CENTIMETER)
        // parameter.frame_parameter.position_rate_second
    )
    first_theorical_curve = linear_interpolation(
        first_takeoff_position,
        THEORICAL_MIDDLE_TAKEOFF_POSITION,
        FIRST_THEORICAL_NB_POINT,
    )
    SECOND_THEORICAL_NB_POINT = int(
        parameter.land_parameter.get_second_land_second_delta(HGT_CENTIMETER)
        // parameter.frame_parameter.position_rate_second
    )
    second_theorical_curve = linear_interpolation(
        THEORICAL_MIDDLE_TAKEOFF_POSITION,
        THEORICAL_END_TAKEOFF_POSITION,
        SECOND_THEORICAL_NB_POINT,
    )
    theorical_curve = first_theorical_curve + second_theorical_curve
    assert len(dance_sequence.drone_positions) == len(theorical_curve)
    assert all(
        [
            np.array_equal(drone_position, theorical_position)
            for drone_position, theorical_position in zip(
                dance_sequence.drone_positions,
                theorical_curve,
            )
        ]
    )
    assert all(dance_sequence.drone_in_air) == True
    assert all(dance_sequence.drone_in_dance) == False
