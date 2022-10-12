import pytest
from ...show_px4.drone_px4.drone_px4 import DronePx4
from ...show_px4.show_px4 import ShowPx4
from .DP_to_DU_procedure import DP_to_DU_procedure
from .data_convertion_format import (
    XyzConvertionStandard,
    RgbwConvertionStandard,
    FireDurationConvertionStandard,
)


ARBITRARY_POSITION_EVENT_FRAME = 360
ARBITRARY_POSITION_EVENT_XYZ = (100, 0, -25)

ARBITRARY_COLOR_EVENT_FRAME = 253
ARBITRARY_COLOR_EVENT_RGBW = (23, 54, 89, 156)


ARBITRARY_FIRE_EVENT_FRAME = 394
ARBITRARY_FIRE_EVENT_CHANEL = 1
ARBITRARY_FIRE_EVENT_DURATION = 25365

ARBITRARY_POSITION_EVENT_FRAME_BIS = 563
ARBITRARY_POSITION_EVENT_XYZ_BIS = (156, 0, -247)

ARBITRARY_COLOR_EVENT_FRAME_BIS = 289
ARBITRARY_COLOR_EVENT_RGBW_BIS = (56, 52, 69, 246)


ARBITRARY_FIRE_EVENT_FRAME_BIS = 987
ARBITRARY_FIRE_EVENT_CHANEL_BIS = 2
ARBITRARY_FIRE_EVENT_DURATION_BIS = 68435


@pytest.fixture
def valid_show_px4() -> ShowPx4:
    drone_px4 = DronePx4(0)

    drone_px4.add_position(ARBITRARY_POSITION_EVENT_FRAME, ARBITRARY_POSITION_EVENT_XYZ)

    drone_px4.add_color(ARBITRARY_COLOR_EVENT_FRAME, ARBITRARY_COLOR_EVENT_RGBW)

    drone_px4.add_fire(
        ARBITRARY_FIRE_EVENT_FRAME,
        ARBITRARY_FIRE_EVENT_CHANEL,
        ARBITRARY_FIRE_EVENT_DURATION,
    )

    drone_px4_bis = DronePx4(1)

    drone_px4_bis.add_position(
        ARBITRARY_POSITION_EVENT_FRAME_BIS, ARBITRARY_POSITION_EVENT_XYZ_BIS
    )

    drone_px4_bis.add_color(
        ARBITRARY_COLOR_EVENT_FRAME_BIS, ARBITRARY_COLOR_EVENT_RGBW_BIS
    )

    drone_px4_bis.add_fire(
        ARBITRARY_FIRE_EVENT_FRAME_BIS,
        ARBITRARY_FIRE_EVENT_CHANEL_BIS,
        ARBITRARY_FIRE_EVENT_DURATION_BIS,
    )
    return ShowPx4([drone_px4, drone_px4_bis])


def test_drone_px4_to_drone_user_procedure_position_events(valid_show_px4: ShowPx4):
    xyz_convertion_standard = XyzConvertionStandard()
    drone_users = DP_to_DU_procedure(
        valid_show_px4,
    )
    assert len(drone_users[0].position_events) == 1
    assert drone_users[0].position_events[0].frame == ARBITRARY_POSITION_EVENT_FRAME
    assert drone_users[0].position_events[
        0
    ].xyz == xyz_convertion_standard.from_px4_xyz_to_user_xyz(
        ARBITRARY_POSITION_EVENT_XYZ
    )

    assert len(drone_users[1].position_events) == 1
    assert drone_users[1].position_events[0].frame == ARBITRARY_POSITION_EVENT_FRAME_BIS
    assert drone_users[1].position_events[
        0
    ].xyz == xyz_convertion_standard.from_px4_xyz_to_user_xyz(
        ARBITRARY_POSITION_EVENT_XYZ_BIS
    )


def test_drone_px4_to_drone_user_procedure_color_events(valid_show_px4: ShowPx4):
    rgbw_convertion_standard = RgbwConvertionStandard()
    drone_users = DP_to_DU_procedure(
        valid_show_px4,
    )

    assert len(drone_users[0].color_events) == 1
    assert drone_users[0].color_events[0].frame == ARBITRARY_COLOR_EVENT_FRAME
    assert drone_users[0].color_events[
        0
    ].rgbw == rgbw_convertion_standard.from_px4_rgbw_to_user_rgbw(
        ARBITRARY_COLOR_EVENT_RGBW
    )

    assert len(drone_users[1].color_events) == 1
    assert drone_users[1].color_events[0].frame == ARBITRARY_COLOR_EVENT_FRAME_BIS
    assert drone_users[1].color_events[
        0
    ].rgbw == rgbw_convertion_standard.from_px4_rgbw_to_user_rgbw(
        ARBITRARY_COLOR_EVENT_RGBW_BIS
    )


def test_drone_px4_to_drone_user_procedure_fire_events(valid_show_px4: ShowPx4):
    fire_duration_convertion_standard = FireDurationConvertionStandard()
    drone_users = DP_to_DU_procedure(
        valid_show_px4,
    )

    assert len(drone_users[0].fire_events) == 1
    assert drone_users[0].fire_events[0].frame == ARBITRARY_FIRE_EVENT_FRAME
    assert drone_users[0].fire_events[0].chanel == ARBITRARY_FIRE_EVENT_CHANEL
    assert drone_users[0].fire_events[
        0
    ].duration == fire_duration_convertion_standard.from_px4_fire_duration_to_user_fire_duration(
        ARBITRARY_FIRE_EVENT_DURATION
    )

    assert len(drone_users[1].fire_events) == 1
    assert drone_users[1].fire_events[0].frame == ARBITRARY_FIRE_EVENT_FRAME_BIS
    assert drone_users[1].fire_events[0].chanel == ARBITRARY_FIRE_EVENT_CHANEL_BIS
    assert drone_users[1].fire_events[
        0
    ].duration == fire_duration_convertion_standard.from_px4_fire_duration_to_user_fire_duration(
        ARBITRARY_FIRE_EVENT_DURATION_BIS
    )
