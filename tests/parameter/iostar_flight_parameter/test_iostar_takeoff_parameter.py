from loader.parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)


def test_takeoff_parameter_methods_values() -> None:
    assert TAKEOFF_PARAMETER.takeoff_duration_second == 10.0
