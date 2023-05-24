from loader.parameters import LAND_PARAMETERS


def test_land_parameters_methods_values() -> None:
    assert LAND_PARAMETERS.get_first_land_second_delta(6.0) == 1.0
    assert LAND_PARAMETERS.get_first_land_second_delta(2.0) == 5
    assert LAND_PARAMETERS.get_first_land_altitude(4.0) == LAND_PARAMETERS.land_safe_hgt
    assert LAND_PARAMETERS.get_first_land_altitude(2.0) == 0

    assert LAND_PARAMETERS.get_second_land_second_delta(6.0) == 7.5
    assert LAND_PARAMETERS.get_second_land_second_delta(2.0) == 0.0
    assert LAND_PARAMETERS.get_second_land_altitude_start(4.0) == LAND_PARAMETERS.land_safe_hgt
    assert LAND_PARAMETERS.get_second_land_altitude_start(2.0) == 0

    assert LAND_PARAMETERS.get_land_second_delta(6.0) == 8.5
    assert LAND_PARAMETERS.get_land_frame_delta(6.0) == 204
