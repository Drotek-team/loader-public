from .json_binary_parameter import JSON_BINARY_PARAMETER


def test_json_binary_parameter_standard_case():
    assert JSON_BINARY_PARAMETER.from_user_xyz_to_px4_xyz((1.0, 2.0, 3.0)) == (
        50,
        25,
        -75,
    )
    assert JSON_BINARY_PARAMETER.from_px4_xyz_to_user_xyz((50, 25, -75,)) == (
        1.0,
        2.0,
        3.0,
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
    assert (
        JSON_BINARY_PARAMETER.from_user_fire_duration_to_px4_fire_duration(1.0) == 1_000
    )
    assert (
        JSON_BINARY_PARAMETER.from_px4_fire_duration_to_user_fire_duration(1_000) == 1.0
    )
