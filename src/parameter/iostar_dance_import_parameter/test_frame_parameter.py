from .frame_parameter import FRAME_PARAMETER


def test_frame_parameter_standard_case():
    assert FRAME_PARAMETER.from_absolute_time_to_absolute_frame(1.0) == 24
    assert FRAME_PARAMETER.from_absolute_frame_to_absolute_time(24) == 1.0
