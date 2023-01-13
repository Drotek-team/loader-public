import pytest
from pydantic import ValidationError

from .show_user import DroneUser


@pytest.fixture
def empty_drone_user():
    return DroneUser(position_events=[], color_events=[], fire_events=[])


def test_position_event_user_standard_case(empty_drone_user: DroneUser):
    empty_drone_user.add_position_event(
        frame=1,
        xyz=(1.0, 2.0, 3.0),
    )
    assert empty_drone_user.position_events[0].frame == 1
    assert empty_drone_user.position_events[0].xyz == (1.0, 2.0, 3.0)


def test_position_event_user_invalid_input(empty_drone_user: DroneUser):
    with pytest.raises(ValidationError):
        empty_drone_user.add_position_event(
            frame=1.0,  # pyright: ignore
            xyz=(1.0, 2.0, 3.0),
        )
    with pytest.raises(ValidationError):
        empty_drone_user.add_position_event(
            frame=1,
            xyz=(1, 2.0, 3.0),
        )


def test_color_event_user_standard_case(empty_drone_user: DroneUser):
    empty_drone_user.add_color_event(
        frame=1,
        rgbw=(1.0, 2.0, 3.0, 4.0),
    )
    assert empty_drone_user.color_events[0].frame == 1
    assert empty_drone_user.color_events[0].rgbw == (1.0, 2.0, 3.0, 4.0)


def test_color_event_user_invalid_input(empty_drone_user: DroneUser):
    with pytest.raises(ValidationError):
        empty_drone_user.add_color_event(
            frame=1.0,  # pyright: ignore
            rgbw=(1.0, 2.0, 3.0, 4.0),
        )
    with pytest.raises(ValidationError):
        empty_drone_user.add_color_event(
            frame=1,
            rgbw=(1, 2.0, 3.0, 4.0),
        )


def test_fire_event_user_standard_case(empty_drone_user: DroneUser):
    empty_drone_user.add_fire_event(
        frame=1,
        chanel=0,
        duration_frame=2,
    )
    assert empty_drone_user.fire_events[0].frame == 1
    assert empty_drone_user.fire_events[0].chanel == 0
    assert empty_drone_user.fire_events[0].duration_frame == 2


def test_fire_event_user_invalid_input(empty_drone_user: DroneUser):
    with pytest.raises(ValidationError):
        empty_drone_user.add_fire_event(
            frame=1.0,  # pyright: ignore
            chanel=0,
            duration_frame=2,
        )
    with pytest.raises(ValidationError):
        empty_drone_user.add_fire_event(
            frame=1,
            chanel=0.0,  # pyright: ignore
            duration_frame=2,
        )
    with pytest.raises(ValidationError):
        empty_drone_user.add_fire_event(
            frame=1,
            chanel=0,
            duration_frame=2.0,  # pyright: ignore
        )
