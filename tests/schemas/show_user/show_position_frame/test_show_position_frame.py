import numpy as np
from loader.parameters import TAKEOFF_PARAMETERS
from loader.schemas.matrix import get_matrix
from loader.schemas.show_user.generate_show_user import ShowUserConfiguration, get_valid_show_user
from loader.schemas.show_user.show_position_frame import ShowPositionFrame


def test_valid_show_flags() -> None:
    show_position_frames = ShowPositionFrame.from_show_user(
        get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2))),
        is_partial=False,
    )
    assert len(show_position_frames) == 171
    assert np.array_equal(
        show_position_frames[0].in_air_positions[0],
        np.array([-0.75, 0.0, 0.0], dtype=np.float64),
    )
    assert np.array_equal(
        show_position_frames[40].in_air_positions[0],
        np.array([-0.75, 0.0, TAKEOFF_PARAMETERS.takeoff_altitude_meter_min], dtype=np.float64),
    )
    assert len(show_position_frames[-1].in_air_positions) == 0


def test_su_to_spf() -> None:
    show_position_frames = ShowPositionFrame.from_show_user(
        get_valid_show_user(ShowUserConfiguration()),
        is_partial=False,
    )
    assert all(len(show_position_frame) == 1 for show_position_frame in show_position_frames)
    assert len(show_position_frames) == 171
    assert [show_position_frame.frame for show_position_frame in show_position_frames] == list(
        range(0, 1022, 6),
    )


def test_show_position_frame_partial_show_user_in_air() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2)))
    show_position_frames = ShowPositionFrame.from_show_user(
        show_user,
        is_partial=True,
    )
    assert all(
        not in_air
        for in_air in show_position_frames[0]._in_air_flags  # pyright: ignore[reportPrivateUsage]
    )
