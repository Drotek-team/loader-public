from .json_binary_parameter import JSON_BINARY_PARAMETER


def test_json_binary_parameter_standard_case():
    assert JSON_BINARY_PARAMETER.from_px4_timecode_to_user_frame(1_000) == 24
    assert JSON_BINARY_PARAMETER.from_user_frame_to_px4_timecode(24) == 1_000

    assert JSON_BINARY_PARAMETER.from_user_position_to_px4_position(1.0) == 100
    assert JSON_BINARY_PARAMETER.from_px4_position_to_user_position(100) == 1.0

    assert JSON_BINARY_PARAMETER.from_user_xyz_to_px4_xyz((1.0, 2.0, 3.0)) == (
        200,
        100,
        -300,
    )
    assert JSON_BINARY_PARAMETER.from_px4_xyz_to_user_xyz((50, 25, -75)) == (
        0.25,
        0.5,
        0.75,
    )

    assert JSON_BINARY_PARAMETER.from_user_rgbw_to_px4_rgbw(
        (
            1 / 3,
            1 / 5,
            1 / 15,
            1 / 17,
        )
    ) == (85, 51, 17, 15)

    assert JSON_BINARY_PARAMETER.from_px4_rgbw_to_user_rgbw((85, 51, 17, 15)) == (
        1 / 3,
        1 / 5,
        1 / 15,
        1 / 17,
    )

    assert JSON_BINARY_PARAMETER.from_user_frame_to_px4_timecode(24) == 1_000
    assert JSON_BINARY_PARAMETER.from_px4_timecode_to_user_frame(1_000) == 24
