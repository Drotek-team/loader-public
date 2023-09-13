from typing import TYPE_CHECKING

import pytest
from hypothesis import given
from loader.parameters.json_binary_parameters import MagicNumber
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

from tests.strategies import slow, st_angle_takeoff, st_matrix

if TYPE_CHECKING:
    import numpy as np
    from numpy.typing import NDArray


@pytest.mark.parametrize("magic_number", list(MagicNumber))
def test_add_position_events_user_standard_case(magic_number: MagicNumber) -> None:
    drone_px4 = DronePx4(0, magic_number)
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
    first_position_event = drone_px4.position_events[0]
    assert first_position_event.frame == 0
    assert first_position_event.xyz == (100, 0, -200)
    second_position_event = drone_px4.position_events[1]
    assert second_position_event.frame == 1
    assert second_position_event.xyz == (400, 300, -500)


@pytest.mark.parametrize("magic_number", list(MagicNumber))
def test_add_color_events_user_standard_case(magic_number: MagicNumber) -> None:
    drone_px4 = DronePx4(0, magic_number)
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
    first_color_event = drone_px4.color_events[0]
    assert first_color_event.frame == 0
    assert first_color_event.rgbw == (0, 255, 0, 255)
    second_color_event = drone_px4.color_events[1]
    assert second_color_event.frame == 1
    assert second_color_event.rgbw == (255, 0, 255, 0)


@pytest.mark.parametrize("magic_number", list(MagicNumber))
def test_add_fire_events_user_standard_case(magic_number: MagicNumber) -> None:
    drone_px4 = DronePx4(0, magic_number)
    fire_events_user = [
        FireEventUser(frame=0, channel=0, duration=42),
        FireEventUser(frame=1, channel=1, duration=83),
    ]
    add_fire_events_user(drone_px4, fire_events_user)
    first_fire_event = drone_px4.fire_events[0]
    assert first_fire_event.frame == 0
    assert first_fire_event.channel_duration == (0, 42)
    second_fire_event = drone_px4.fire_events[1]
    assert second_fire_event.frame == 1
    assert second_fire_event.channel_duration == (1, 83)


def test_drone_user_to_drone_px4_standard_case() -> None:
    drone_user = DroneUser(
        index=0,
        position_events=[PositionEventUser(frame=0, xyz=(0.0, 1.0, 2.0))],
        color_events=[ColorEventUser(frame=0, rgbw=(0.0, 1.0, 0.0, 1.0))],
        fire_events=[FireEventUser(frame=0, channel=0, duration=42)],
    )
    drone_px4 = drone_user_to_drone_px4(drone_user)
    assert drone_px4.index == 0
    assert drone_px4.position_events[0].frame == 0
    assert drone_px4.position_events[0].xyz == (100, 0, -200)
    assert drone_px4.color_events[0].frame == 0
    assert drone_px4.color_events[0].rgbw == (0, 255, 0, 255)
    assert drone_px4.fire_events[0].frame == 0
    assert drone_px4.fire_events[0].channel_duration == (0, 42)


@given(
    matrix=st_matrix(),
    angle_takeoff=st_angle_takeoff,
)
@slow
def test_su_to_sp_standard_case(
    matrix: "NDArray[np.intp]",
    angle_takeoff: float,
) -> None:
    show_user = get_valid_show_user(
        ShowUserConfiguration(matrix=matrix, angle_takeoff=angle_takeoff),
    )
    new_show_user = ShowUser.from_autopilot_format(
        DronePx4.from_show_user(show_user),
        angle_takeoff=show_user.angle_takeoff,
        step=show_user.step,
    )
    assert show_user == new_show_user
