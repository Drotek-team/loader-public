from loader.parameters import FRAME_PARAMETERS


def test_frame_parameters_standard_case() -> None:
    assert FRAME_PARAMETERS.from_second_to_frame(1.0) == 24
    assert FRAME_PARAMETERS.from_frame_to_second(24) == 1.0
