from loader.parameters import JSON_BINARY_PARAMETERS, Bound


def test_json_binary_parameters_standard_case() -> None:
    assert JSON_BINARY_PARAMETERS.position_event_format == ">Ihhh"
    assert JSON_BINARY_PARAMETERS.color_event_format == ">IBBBB"
    assert JSON_BINARY_PARAMETERS.fire_event_format == ">IBB"

    assert JSON_BINARY_PARAMETERS.timecode_value_bound == Bound(0, 2**32 - 1)
    assert JSON_BINARY_PARAMETERS.coordinate_value_bound == Bound(
        -(2**15),
        2**15 - 1,
    )
    assert JSON_BINARY_PARAMETERS.chrome_value_bound == Bound(0, 2**8 - 1)
    assert JSON_BINARY_PARAMETERS.fire_chanel_value_bound == Bound(0, 2)
    assert JSON_BINARY_PARAMETERS.fire_duration_value_bound == Bound(0, 2**8 - 1)

    assert JSON_BINARY_PARAMETERS.from_px4_timecode_to_user_frame(1_000) == 24
    assert JSON_BINARY_PARAMETERS.from_user_frame_to_px4_timecode(24) == 1_000

    assert JSON_BINARY_PARAMETERS.from_user_position_to_px4_position(1.0) == 100
    assert JSON_BINARY_PARAMETERS.from_px4_position_to_user_position(100) == 1.0

    assert JSON_BINARY_PARAMETERS.from_user_xyz_to_px4_xyz((1.0, 2.0, 3.0)) == (
        200,
        100,
        -300,
    )
    assert JSON_BINARY_PARAMETERS.from_px4_xyz_to_user_xyz((50, 25, -75)) == (
        0.25,
        0.5,
        0.75,
    )

    assert JSON_BINARY_PARAMETERS.from_user_rgbw_to_px4_rgbw(
        (
            1 / 3,
            1 / 5,
            1 / 15,
            1 / 17,
        ),
    ) == (85, 51, 17, 15)

    assert JSON_BINARY_PARAMETERS.from_px4_rgbw_to_user_rgbw((85, 51, 17, 15)) == (
        1 / 3,
        1 / 5,
        1 / 15,
        1 / 17,
    )

    assert JSON_BINARY_PARAMETERS.from_user_frame_to_px4_timecode(24) == 1_000
    assert JSON_BINARY_PARAMETERS.from_px4_timecode_to_user_frame(1_000) == 24
    assert JSON_BINARY_PARAMETERS.from_user_frame_to_px4_timecode(24) == 1_000
    assert JSON_BINARY_PARAMETERS.from_px4_timecode_to_user_frame(1_000) == 24
