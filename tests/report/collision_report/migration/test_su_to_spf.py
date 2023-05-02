import numpy as np
from loader.parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from loader.report.collision_report.show_position_frames_collision_report import (
    su_to_spf,
)
from loader.show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)


def test_valid_show_flags() -> None:
    show_position_frames = su_to_spf(
        get_valid_show_user(ShowUserConfiguration(nb_x=2)),
    )
    assert len(show_position_frames.show_position_frames) == 1022
    assert np.array_equal(
        show_position_frames.show_position_frames[0].in_air_positions[0],
        np.array([-0.75, 0.0, 0.0], dtype=np.float64),
    )
    assert np.array_equal(
        show_position_frames.show_position_frames[240].in_air_positions[0],
        np.array(
            [-0.75, 0.0, TAKEOFF_PARAMETER.takeoff_altitude_meter_min],
            dtype=np.float64,
        ),
    )
    assert len(show_position_frames.show_position_frames[-1].in_air_positions) == 0


def test_su_to_spf() -> None:
    show_position_frames = su_to_spf(get_valid_show_user(ShowUserConfiguration()))
    assert all(
        len(show_position_frame) == 1
        for show_position_frame in show_position_frames.show_position_frames
    )
    assert len(show_position_frames.show_position_frames) == 1022
    assert [
        show_position_frame.frame
        for show_position_frame in show_position_frames.show_position_frames
    ] == list(range(1022))
