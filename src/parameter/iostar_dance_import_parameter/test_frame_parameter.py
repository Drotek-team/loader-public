from .frame_parameter import FRAME_PARAMETER


def test_frame_parameter_standard_case():
    assert FRAME_PARAMETER.from_position_frame_to_absolute_frame(4) == 24
    assert FRAME_PARAMETER.from_position_frame_to_absolute_time(4) == 1.0
    assert FRAME_PARAMETER.from_absolute_time_to_position_frame(1.0) == 4

    assert FRAME_PARAMETER.from_color_frame_to_absolute_frame(4) == 4
    assert FRAME_PARAMETER.from_color_frame_to_absolute_time(24) == 1.0
    assert FRAME_PARAMETER.from_absolute_time_to_color_frame(1.0) == 24

    assert FRAME_PARAMETER.from_fire_frame_to_absolute_frame(4) == 4
    assert FRAME_PARAMETER.from_fire_frame_to_absolute_time(24) == 1.0
    assert FRAME_PARAMETER.from_absolute_time_to_fire_frame(1.0) == 24
