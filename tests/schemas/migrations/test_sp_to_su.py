from typing import List

import pytest
from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS, MagicNumber
from loader.schemas.drone_px4 import DronePx4
from loader.schemas.show_user.show_user import ShowUser

ARBITRARY_POSITION_EVENT_FRAME = 9
ARBITRARY_POSITION_EVENT_XYZ = (100, 0, -25)

ARBITRARY_COLOR_EVENT_FRAME = 253
ARBITRARY_COLOR_EVENT_RGBW = (23, 54, 89, 156)


ARBITRARY_FIRE_EVENT_FRAME = 394
ARBITRARY_FIRE_EVENT_CHANEL = 1
ARBITRARY_FIRE_EVENT_DURATION = 25365

ARBITRARY_POSITION_EVENT_FRAME_BIS = 14
ARBITRARY_POSITION_EVENT_XYZ_BIS = (156, 0, -247)

ARBITRARY_COLOR_EVENT_FRAME_BIS = 289
ARBITRARY_COLOR_EVENT_RGBW_BIS = (56, 52, 69, 246)


ARBITRARY_FIRE_EVENT_FRAME_BIS = 987
ARBITRARY_FIRE_EVENT_CHANEL_BIS = 2
ARBITRARY_FIRE_EVENT_DURATION_BIS = 68435


@pytest.fixture
def valid_autopilot_format(request: pytest.FixtureRequest) -> List[DronePx4]:
    drone_px4 = DronePx4(0, request.param)

    drone_px4.add_position(ARBITRARY_POSITION_EVENT_FRAME, ARBITRARY_POSITION_EVENT_XYZ)

    drone_px4.add_color(ARBITRARY_COLOR_EVENT_FRAME, ARBITRARY_COLOR_EVENT_RGBW)

    drone_px4.add_fire(
        ARBITRARY_FIRE_EVENT_FRAME,
        ARBITRARY_FIRE_EVENT_CHANEL,
        ARBITRARY_FIRE_EVENT_DURATION,
    )

    drone_px4_bis = DronePx4(1, request.param)

    drone_px4_bis.add_position(
        ARBITRARY_POSITION_EVENT_FRAME_BIS,
        ARBITRARY_POSITION_EVENT_XYZ_BIS,
    )

    drone_px4_bis.add_color(
        ARBITRARY_COLOR_EVENT_FRAME_BIS,
        ARBITRARY_COLOR_EVENT_RGBW_BIS,
    )

    drone_px4_bis.add_fire(
        ARBITRARY_FIRE_EVENT_FRAME_BIS,
        ARBITRARY_FIRE_EVENT_CHANEL_BIS,
        ARBITRARY_FIRE_EVENT_DURATION_BIS,
    )
    return [drone_px4, drone_px4_bis]


@pytest.mark.parametrize("valid_autopilot_format", list(MagicNumber), indirect=True)
def test_drone_px4_to_drone_user_position_events(valid_autopilot_format: List[DronePx4]) -> None:
    show_user = ShowUser.from_autopilot_format(valid_autopilot_format, angle_takeoff=0, step=1)
    drone_users = show_user.drones_user
    assert len(drone_users[0].position_events) == 1
    assert drone_users[0].position_events[0].frame == ARBITRARY_POSITION_EVENT_FRAME
    assert drone_users[0].position_events[0].xyz == JSON_BINARY_PARAMETERS.from_px4_xyz_to_user_xyz(
        ARBITRARY_POSITION_EVENT_XYZ,
    )

    assert len(drone_users[1].position_events) == 1
    assert drone_users[1].position_events[0].frame == ARBITRARY_POSITION_EVENT_FRAME_BIS
    assert drone_users[1].position_events[0].xyz == JSON_BINARY_PARAMETERS.from_px4_xyz_to_user_xyz(
        ARBITRARY_POSITION_EVENT_XYZ_BIS,
    )


@pytest.mark.parametrize("valid_autopilot_format", list(MagicNumber), indirect=True)
def test_drone_px4_to_drone_user_color_events(
    valid_autopilot_format: List[DronePx4],
) -> None:
    show_user = ShowUser.from_autopilot_format(valid_autopilot_format, angle_takeoff=0, step=1)
    drone_users = show_user.drones_user

    assert len(drone_users[0].color_events) == 1
    assert drone_users[0].color_events[0].frame == ARBITRARY_COLOR_EVENT_FRAME
    assert drone_users[0].color_events[0].rgbw == JSON_BINARY_PARAMETERS.from_px4_rgbw_to_user_rgbw(
        ARBITRARY_COLOR_EVENT_RGBW,
    )
    assert len(drone_users[1].color_events) == 1
    assert drone_users[1].color_events[0].frame == ARBITRARY_COLOR_EVENT_FRAME_BIS
    assert drone_users[1].color_events[0].rgbw == JSON_BINARY_PARAMETERS.from_px4_rgbw_to_user_rgbw(
        ARBITRARY_COLOR_EVENT_RGBW_BIS,
    )


@pytest.mark.parametrize("valid_autopilot_format", list(MagicNumber), indirect=True)
def test_drone_px4_to_drone_user_fire_events(
    valid_autopilot_format: List[DronePx4],
) -> None:
    show_user = ShowUser.from_autopilot_format(valid_autopilot_format, angle_takeoff=0, step=1)
    drone_users = show_user.drones_user

    assert len(drone_users[0].fire_events) == 1
    assert drone_users[0].fire_events[0].frame == ARBITRARY_FIRE_EVENT_FRAME
    assert drone_users[0].fire_events[0].channel == ARBITRARY_FIRE_EVENT_CHANEL
    assert drone_users[0].fire_events[0].duration == ARBITRARY_FIRE_EVENT_DURATION

    assert len(drone_users[1].fire_events) == 1
    assert drone_users[1].fire_events[0].frame == ARBITRARY_FIRE_EVENT_FRAME_BIS
    assert drone_users[1].fire_events[0].channel == ARBITRARY_FIRE_EVENT_CHANEL_BIS
    assert drone_users[1].fire_events[0].duration == ARBITRARY_FIRE_EVENT_DURATION_BIS
