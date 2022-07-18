import numpy as np
import pytest

from ....parameter.parameter import Parameter
from ....show_simulation.dance_simulation.convert_drone_to_dance_simulation import (
    land_simulation,
)
from ....show_simulation.dance_simulation.position_simulation import (
    linear_interpolation,
)


def test_land_simulation_first_case():
    parameter = Parameter()
    parameter.load_iostar_parameter()
    parameter.load_export_parameter()
    X_CENTIMETER = 2_00
    Y_CENTIMETER = 2_00
    HGT_CENTIMETER = -1_00
    first_takeoff_position = (X_CENTIMETER, Y_CENTIMETER, HGT_CENTIMETER)
    dance_sequence = land_simulation(
        first_takeoff_position,
        parameter.timecode_parameter,
        parameter.land_parameter,
        parameter.json_convertion_constant,
    )
    THEORICAL_LAST_TAKEOFF_POSITION = (X_CENTIMETER, Y_CENTIMETER, 0)
    THEORICAL_NB_POINT = (
        parameter.land_parameter.get_first_land_timecode_delta(HGT_CENTIMETER)
        // parameter.timecode_parameter.position_timecode_rate
    )
    theorical_curve = linear_interpolation(
        first_takeoff_position,
        THEORICAL_LAST_TAKEOFF_POSITION,
        THEORICAL_NB_POINT,
        parameter.json_convertion_constant,
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
    parameter.load_iostar_parameter()
    parameter.load_export_parameter()
    X_CENTIMETER = 2_00
    Y_CENTIMETER = 2_00
    HGT_CENTIMETER = 5_00
    first_takeoff_position = (X_CENTIMETER, Y_CENTIMETER, HGT_CENTIMETER)
    dance_sequence = land_simulation(
        first_takeoff_position,
        parameter.timecode_parameter,
        parameter.land_parameter,
        parameter.json_convertion_constant,
    )
    THEORICAL_MIDDLE_TAKEOFF_POSITION = (
        X_CENTIMETER,
        Y_CENTIMETER,
        parameter.land_parameter.land_safe_hgt,
    )
    THEORICAL_END_TAKEOFF_POSITION = (
        X_CENTIMETER,
        Y_CENTIMETER,
        0,
    )
    FIRST_THEORICAL_NB_POINT = (
        parameter.land_parameter.get_first_land_timecode_delta(HGT_CENTIMETER)
        // parameter.timecode_parameter.position_timecode_rate
    )
    first_theorical_curve = linear_interpolation(
        first_takeoff_position,
        THEORICAL_MIDDLE_TAKEOFF_POSITION,
        FIRST_THEORICAL_NB_POINT,
        parameter.json_convertion_constant,
    )
    SECOND_THEORICAL_NB_POINT = (
        parameter.land_parameter.get_second_land_timecode_delta(HGT_CENTIMETER)
        // parameter.timecode_parameter.position_timecode_rate
    )
    second_theorical_curve = linear_interpolation(
        THEORICAL_MIDDLE_TAKEOFF_POSITION,
        THEORICAL_END_TAKEOFF_POSITION,
        SECOND_THEORICAL_NB_POINT,
        parameter.json_convertion_constant,
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
