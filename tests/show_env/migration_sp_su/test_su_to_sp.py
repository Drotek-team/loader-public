from hypothesis import given
from loader.schemas.drone_px4 import DronePx4
from loader.schemas.drone_px4.drone_px4 import (
    add_color_events_user,
    add_fire_events_user,
    add_position_events_user,
    drone_user_to_drone_px4,
)
from loader.schemas.show_user import ColorEventUser, DroneUser, FireEventUser, PositionEventUser
from loader.schemas.show_user.generate_show_user import ShowUserConfiguration, get_valid_show_user
from loader.schemas.show_user.show_user import ShowUser

from tests.strategies import slow, st_nb_drone_per_family, st_nb_x, st_nb_y


def test_add_position_events_user_standard_case() -> None:
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


def test_add_color_events_user_standard_case() -> None:
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


def test_add_fire_events_user_standard_case() -> None:
    drone_px4 = DronePx4(0)
    fire_events_user = [
        FireEventUser(frame=0, chanel=0, duration=41),
        FireEventUser(frame=1, chanel=1, duration=83),
    ]
    add_fire_events_user(drone_px4, fire_events_user)
    first_fire_event = drone_px4.fire_events.get_fire_event_by_index(0)
    assert first_fire_event.timecode == 0
    assert first_fire_event.chanel_duration == (0, 41)
    second_fire_event = drone_px4.fire_events.get_fire_event_by_index(1)
    assert second_fire_event.timecode == 41
    assert second_fire_event.chanel_duration == (1, 83)


def test_drone_user_to_drone_px4_standard_case() -> None:
    drone_user = DroneUser(
        index=0,
        position_events=[PositionEventUser(frame=0, xyz=(0.0, 1.0, 2.0))],
        color_events=[ColorEventUser(frame=0, rgbw=(0.0, 1.0, 0.0, 1.0))],
        fire_events=[FireEventUser(frame=0, chanel=0, duration=41)],
    )
    drone_px4 = drone_user_to_drone_px4(drone_user)
    assert drone_px4.index == 0
    assert drone_px4.position_events.get_position_event_by_index(0).timecode == 0
    assert drone_px4.position_events.get_position_event_by_index(0).xyz == (100, 0, -200)
    assert drone_px4.color_events.get_color_event_by_index(0).timecode == 0
    assert drone_px4.color_events.get_color_event_by_index(0).rgbw == (0, 255, 0, 255)
    assert drone_px4.fire_events.get_fire_event_by_index(0).timecode == 0
    assert drone_px4.fire_events.get_fire_event_by_index(0).chanel_duration == (0, 41)


@given(
    nb_x=st_nb_x,
    nb_y=st_nb_y,
    nb_drone_per_family=st_nb_drone_per_family,
)
@slow
def test_su_to_sp_standard_case(nb_x: int, nb_y: int, nb_drone_per_family: int) -> None:
    show_user = get_valid_show_user(
        ShowUserConfiguration(
            nb_x=nb_x,
            nb_y=nb_y,
            nb_drone_per_family=nb_drone_per_family,
        ),
    )
    new_show_user = ShowUser.from_autopilot_format(DronePx4.from_show_user(show_user))
    assert show_user == new_show_user
