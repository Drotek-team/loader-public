from loader.parameter.iostar_dance_import_parameter.frame_parameter import (
    FRAME_PARAMETER,
)


def test_frame_parameter_standard_case() -> None:
    assert FRAME_PARAMETER.from_second_to_frame(1.0) == 24
    assert FRAME_PARAMETER.from_frame_to_second(24) == 1.0
