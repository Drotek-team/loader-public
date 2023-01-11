import pytest
from pydantic import ValidationError

from .show_user import ColorEventUser, FireEventUser, PositionEventUser


def test_position_event_user_standard_case():
    position_event_user = PositionEventUser(
        frame=1,
        xyz=(1.0, 2.0, 3.0),
    )
    assert position_event_user.frame == 1
    assert position_event_user.xyz == (1.0, 2.0, 3.0)


def test_position_event_user_invalid_frame_type():
    with pytest.raises(ValidationError):
        PositionEventUser(
            frame=1.0,
            xyz=(1.0, 2.0, 3.0),
        )


def test_position_event_user_invalid_xyz_type():
    with pytest.raises(ValidationError):
        PositionEventUser(
            frame=1,
            xyz=(1, 2.0, 3.0),
        )


def test_color_event_user_standard_case():
    color_event_user = ColorEventUser(
        frame=1,
        rgbw=(1.0, 2.0, 3.0, 4.0),
    )
    assert color_event_user.frame == 1
    assert color_event_user.rgbw == (1.0, 2.0, 3.0, 4.0)


def test_color_event_user_invalid_frame_type():
    with pytest.raises(ValidationError):
        ColorEventUser(
            frame=1.0,
            rgbw=(1.0, 2.0, 3.0, 4.0),
        )


def test_color_event_user_invalid_xyz_type():
    with pytest.raises(ValidationError):
        ColorEventUser(
            frame=1,
            xyz=(1, 2.0, 3.0, 4.0),
        )


def test_fire_event_user_standard_case():
    fire_event_user = FireEventUser(
        frame=1,
        chanel=0,
        duration_frame=2,
    )
    assert fire_event_user.frame == 1
    assert fire_event_user.chanel == 0
    assert fire_event_user.duration_frame == 2


def test_fire_event_user_invalid_frame_type():
    with pytest.raises(ValidationError):
        FireEventUser(
            frame=1.0,
            chanel=0,
            duration_frame=2,
        )


def test_fire_event_user_invalid_chanel_type():
    with pytest.raises(ValidationError):
        FireEventUser(
            frame=1,
            chanel=0.0,
            duration_frame=2,
        )


def test_fire_event_user_invalid_duration_frame_type():
    with pytest.raises(ValidationError):
        FireEventUser(
            frame=1,
            chanel=0,
            duration_frame=2.0,
        )
