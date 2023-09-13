import struct

from loader.reports import DanceSizeInfraction
from loader.schemas.drone_px4 import DronePx4
from loader.schemas.drone_px4.events import ColorEvents, FireEvents, PositionEvents
from loader.schemas.drone_px4.events.magic_number import MagicNumber

DANCE_BASIC_SIZE = 34
POSITION_EVENT_SIZE = struct.calcsize(PositionEvents(MagicNumber.old).format_)
COLOR_EVENT_SIZE = struct.calcsize(ColorEvents(MagicNumber.old).format_)
FIRE_EVENT_SIZE = struct.calcsize(FireEvents(MagicNumber.old).format_)


def test_dance_size_information_standard_case() -> None:
    dance_size_information = DanceSizeInfraction(
        drone_index=0,
        dance_size=50,
        position_percent=12,
        color_percent=24,
        fire_percent=36,
    )
    assert dance_size_information.total_percent == 72


def test_get_dance_size_information_standard_case() -> None:
    empty_drone_px4 = DronePx4(0, MagicNumber.old)

    assert DanceSizeInfraction.generate(empty_drone_px4) == DanceSizeInfraction(
        drone_index=0,
        dance_size=7,
        position_percent=0,
        color_percent=0,
        fire_percent=0,
    )

    for _ in range(1_000):
        empty_drone_px4.add_position(0, (0, 0, 0))
    assert DanceSizeInfraction.generate(empty_drone_px4) == DanceSizeInfraction(
        drone_index=0,
        dance_size=10_016,
        position_percent=10,
        color_percent=0,
        fire_percent=0,
    )

    for _ in range(1_000):
        empty_drone_px4.add_color(0, (0, 0, 0, 0))
    assert DanceSizeInfraction.generate(empty_drone_px4) == DanceSizeInfraction(
        drone_index=0,
        dance_size=18_025,
        position_percent=10,
        color_percent=8,
        fire_percent=0,
    )

    for _ in range(1_000):
        empty_drone_px4.add_fire(0, 0, 0)
    assert DanceSizeInfraction.generate(empty_drone_px4) == DanceSizeInfraction(
        drone_index=0,
        dance_size=24_034,
        position_percent=10,
        color_percent=8,
        fire_percent=6,
    )
