import numpy as np

from ....parameter.parameter import Parameter
from ....show_simulation.dance_simulation.convert_trajectory_to_dance_simulation import (
    land_simulation,
)
from ....show_simulation.dance_simulation.position_simulation import (
    linear_interpolation,
)


def test_land_simulation_first_case():
    parameter = Parameter()
    parameter.load_iostar_parameter()
    parameter.load_export_parameter()
    X_METER = 2
    Y_METER = 2
    HGT_CENTIMETER = 1
    first_takeoff_position = (X_METER, Y_METER, HGT_CENTIMETER)

    dance_sequence = land_simulation(
        first_takeoff_position,
        parameter.timecode_parameter,
        parameter.land_parameter,
    )
    THEORICAL_LAST_TAKEOFF_POSITION = (X_METER, Y_METER, 0)
    THEORICAL_NB_POINT = int(
        parameter.land_parameter.get_first_land_second_delta(HGT_CENTIMETER)
        // parameter.timecode_parameter.position_second_rate
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
    parameter.load_iostar_parameter()
    parameter.load_export_parameter()
    X_METER = 2
    Y_METER = 2
    HGT_CENTIMETER = 5
    first_takeoff_position = (X_METER, Y_METER, HGT_CENTIMETER)
    dance_sequence = land_simulation(
        first_takeoff_position,
        parameter.timecode_parameter,
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
        // parameter.timecode_parameter.position_second_rate
    )
    first_theorical_curve = linear_interpolation(
        first_takeoff_position,
        THEORICAL_MIDDLE_TAKEOFF_POSITION,
        FIRST_THEORICAL_NB_POINT,
    )
    SECOND_THEORICAL_NB_POINT = int(
        parameter.land_parameter.get_second_land_second_delta(HGT_CENTIMETER)
        // parameter.timecode_parameter.position_second_rate
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
