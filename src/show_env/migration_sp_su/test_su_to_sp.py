from hypothesis import given
from hypothesis import strategies as st

from ..show_px4.drone_px4.drone_px4 import DronePx4
from ..show_user.generate_show_user import ShowUserConfiguration, get_valid_show_user
from ..show_user.show_user import (
    ColorEventUser,
    DroneUser,
    FireEventUser,
    PositionEventUser,
)
from .sp_to_su import sp_to_su
from .su_to_sp import (
    add_color_events_user,
    add_fire_events_user,
    add_position_events_user,
    drone_user_to_drone_px4,
    su_to_sp,
)


def test_add_position_events_user_standard_case():
    drone_px4 = DronePx4(0)
    position_events_user = [
        PositionEventUser(
            frame=0,
            xyz=(0.0, 1.0, 2.0),
        ),
        PositionEventUser(
            frame=1,
            xyz=(3.0, 4.0, 5.0),
        ),
    ]
    add_position_events_user(drone_px4, position_events_user)
    first_position_event = drone_px4.position_events.get_position_event_by_index(0)
    assert first_position_event.timecode == 0
    assert first_position_event.xyz == (100, 0, -200)
    second_position_event = drone_px4.position_events.get_position_event_by_index(1)
    assert second_position_event.timecode == 41
    assert second_position_event.xyz == (400, 300, -500)


def test_add_color_events_user_standard_case():
    drone_px4 = DronePx4(0)
    color_events_user = [
        ColorEventUser(
            frame=0,
            rgbw=(0.0, 1.0, 0.0, 1.0),
        ),
        ColorEventUser(
            frame=1,
            rgbw=(1.0, 0.0, 1.0, 0.0),
        ),
    ]
    add_color_events_user(drone_px4, color_events_user)
    first_color_event = drone_px4.color_events.get_color_event_by_index(0)
    assert first_color_event.timecode == 0
    assert first_color_event.rgbw == (0, 255, 0, 255)
    second_color_event = drone_px4.color_events.get_color_event_by_index(1)
    assert second_color_event.timecode == 41
    assert second_color_event.rgbw == (255, 0, 255, 0)


def test_add_fire_events_user_standard_case():
    drone_px4 = DronePx4(0)
    fire_events_user = [
        FireEventUser(
            frame=0,
            chanel=0,
            duration_frame=1,
        ),
        FireEventUser(
            frame=1,
            chanel=1,
            duration_frame=2,
        ),
    ]
    add_fire_events_user(drone_px4, fire_events_user)
    first_fire_event = drone_px4.fire_events.get_fire_event_by_index(0)
    assert first_fire_event.timecode == 0
    assert first_fire_event.chanel_duration == (0, 41)
    second_fire_event = drone_px4.fire_events.get_fire_event_by_index(1)
    assert second_fire_event.timecode == 41
    assert second_fire_event.chanel_duration == (1, 83)


def test_drone_user_to_drone_px4_standard_case():
    drone_user = DroneUser(
        position_events=[
            PositionEventUser(
                frame=0,
                xyz=(0.0, 1.0, 2.0),
            ),
        ],
        color_events=[
            ColorEventUser(
                frame=0,
                rgbw=(0.0, 1.0, 0.0, 1.0),
            ),
        ],
        fire_events=[
            FireEventUser(
                frame=0,
                chanel=0,
                duration_frame=1,
            ),
        ],
    )
    drone_px4 = drone_user_to_drone_px4(drone_user, 0)
    assert drone_px4.position_events.get_position_event_by_index(0).timecode == 0
    assert drone_px4.position_events.get_position_event_by_index(0).xyz == (
        100,
        0,
        -200,
    )
    assert drone_px4.color_events.get_color_event_by_index(0).timecode == 0
    assert drone_px4.color_events.get_color_event_by_index(0).rgbw == (0, 255, 0, 255)
    assert drone_px4.fire_events.get_fire_event_by_index(0).timecode == 0
    assert drone_px4.fire_events.get_fire_event_by_index(0).chanel_duration == (0, 41)


@given(
    nb_x=st.integers(1, 3),
    nb_y=st.integers(1, 3),
    nb_drone_per_family=st.integers(1, 3),
)
def test_su_to_sp_standard_case(nb_x: int, nb_y: int, nb_drone_per_family: int):
    show_user = get_valid_show_user(
        ShowUserConfiguration(
            nb_x=nb_x,
            nb_y=nb_y,
            nb_drone_per_family=nb_drone_per_family,
        )
    )
    new_show_user = sp_to_su(su_to_sp(show_user))
    assert show_user == new_show_user