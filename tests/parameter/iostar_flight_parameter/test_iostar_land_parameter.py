from loader.parameter.iostar_flight_parameter.iostar_land_parameter import (
    LAND_PARAMETER,
)


def test_land_parameter_methods_values() -> None:
    assert LAND_PARAMETER.get_first_land_second_delta(6.0) == 1.0
    assert LAND_PARAMETER.get_first_land_second_delta(2.0) == 5
    assert LAND_PARAMETER.get_first_land_altitude(4.0) == LAND_PARAMETER.land_safe_hgt
    assert LAND_PARAMETER.get_first_land_altitude(2.0) == 0

    assert LAND_PARAMETER.get_second_land_second_delta(6.0) == 7.5
    assert LAND_PARAMETER.get_second_land_second_delta(2.0) == 0.0
    assert LAND_PARAMETER.get_second_land_altitude_start(4.0) == LAND_PARAMETER.land_safe_hgt
    assert LAND_PARAMETER.get_second_land_altitude_start(2.0) == 0

    assert LAND_PARAMETER.get_land_second_delta(6.0) == 8.5
    assert LAND_PARAMETER.get_land_frame_delta(6.0) == 204
