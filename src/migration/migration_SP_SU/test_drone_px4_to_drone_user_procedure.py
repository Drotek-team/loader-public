import pytest
from ...show_px4.drone_px4.drone_px4 import DronePx4
from .SP_to_SU_procedure import drone_px4_to_drone_user_procedure
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


@pytest.fixture
def valid_drone_px4() -> DronePx4:
    drone_px4 = DronePx4(0)
    ### Add positions
    drone_px4.add_position(ARBITRARY_POSITION_EVENT_FRAME, ARBITRARY_POSITION_EVENT_XYZ)

    ### Add colors
    drone_px4.add_color(ARBITRARY_COLOR_EVENT_FRAME, ARBITRARY_COLOR_EVENT_RGBW)

    ### Add fires
    drone_px4.add_fire(
        ARBITRARY_FIRE_EVENT_FRAME,
        ARBITRARY_FIRE_EVENT_CHANEL,
        ARBITRARY_FIRE_EVENT_DURATION,
    )
    return drone_px4


def test_drone_px4_to_drone_user_procedure_position_events(valid_drone_px4: DronePx4):
    xyz_convertion_standard = XyzConvertionStandard()
    rgbw_convertion_standard = RgbwConvertionStandard()
    fire_duration_convertion_standard = FireDurationConvertionStandard()

    drone_user = drone_px4_to_drone_user_procedure(
        valid_drone_px4,
        xyz_convertion_standard,
        rgbw_convertion_standard,
        fire_duration_convertion_standard,
    )
    assert len(drone_user.position_events) == 1
    assert drone_user.position_events[0].frame == ARBITRARY_POSITION_EVENT_FRAME
    assert drone_user.position_events[
        0
    ].xyz == xyz_convertion_standard.from_px4_xyz_to_user_xyz(
        ARBITRARY_POSITION_EVENT_XYZ
    )


def test_drone_px4_to_drone_user_procedure_color_events(valid_drone_px4: DronePx4):
    xyz_convertion_standard = XyzConvertionStandard()
    rgbw_convertion_standard = RgbwConvertionStandard()
    fire_duration_convertion_standard = FireDurationConvertionStandard()

    drone_user = drone_px4_to_drone_user_procedure(
        valid_drone_px4,
        xyz_convertion_standard,
        rgbw_convertion_standard,
        fire_duration_convertion_standard,
    )
    ### Color Events Check
    assert len(drone_user.color_events) == 1
    assert drone_user.color_events[0].frame == ARBITRARY_COLOR_EVENT_FRAME
    assert drone_user.color_events[
        0
    ].rgbw == rgbw_convertion_standard.from_px4_rgbw_to_user_rgbw(
        ARBITRARY_COLOR_EVENT_RGBW
    )


def test_drone_px4_to_drone_user_procedure_fire_events(valid_drone_px4: DronePx4):
    xyz_convertion_standard = XyzConvertionStandard()
    rgbw_convertion_standard = RgbwConvertionStandard()
    fire_duration_convertion_standard = FireDurationConvertionStandard()

    drone_user = drone_px4_to_drone_user_procedure(
        valid_drone_px4,
        xyz_convertion_standard,
        rgbw_convertion_standard,
        fire_duration_convertion_standard,
    )
    ### Fire Events Check
    assert len(drone_user.fire_events) == 1
    assert drone_user.fire_events[0].frame == ARBITRARY_FIRE_EVENT_FRAME
    assert drone_user.fire_events[0].chanel == ARBITRARY_FIRE_EVENT_CHANEL
    assert drone_user.fire_events[
        0
    ].duration == fire_duration_convertion_standard.from_px4_fire_duration_to_user_fire_duration(
        ARBITRARY_FIRE_EVENT_DURATION
    )
