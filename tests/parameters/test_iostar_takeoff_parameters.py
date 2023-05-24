from loader.parameters import TAKEOFF_PARAMETERS


def test_takeoff_parameters_methods_values() -> None:
    assert TAKEOFF_PARAMETERS.takeoff_duration_second == 10.0
