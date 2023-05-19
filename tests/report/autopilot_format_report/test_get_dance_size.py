import struct

from loader.reports import (
    DanceSizeInformation,
    get_dance_size_information,
)
from loader.shows.drone_px4 import (
    DronePx4,
)
from loader.shows.drone_px4.events import (
    ColorEvents,
    FireEvents,
    PositionEvents,
)

DANCE_BASIC_SIZE = 34
POSITION_EVENT_SIZE = struct.calcsize(PositionEvents().format_)
COLOR_EVENT_SIZE = struct.calcsize(ColorEvents().format_)
FIRE_EVENT_SIZE = struct.calcsize(FireEvents().format_)


def test_dance_size_information_standard_case() -> None:
    dance_size_information = DanceSizeInformation(
        drone_index=0,
        dance_size=50,
        position_events_size_pct=12,
        color_events_size_pct=24,
        fire_events_size_pct=36,
    )
    assert dance_size_information.total_events_size_pct == 72


def test_get_dance_size_information_standard_case() -> None:
    empty_drone_px4 = DronePx4(0)

    assert get_dance_size_information(empty_drone_px4) == DanceSizeInformation(
        drone_index=0,
        dance_size=7,
        position_events_size_pct=0,
        color_events_size_pct=0,
        fire_events_size_pct=0,
    )

    for _ in range(1_000):
        empty_drone_px4.add_position(0, (0, 0, 0))
    assert get_dance_size_information(empty_drone_px4) == DanceSizeInformation(
        drone_index=0,
        dance_size=10_016,
        position_events_size_pct=10,
        color_events_size_pct=0,
        fire_events_size_pct=0,
    )

    for _ in range(1_000):
        empty_drone_px4.add_color(0, (0, 0, 0, 0))
    assert get_dance_size_information(empty_drone_px4) == DanceSizeInformation(
        drone_index=0,
        dance_size=18_025,
        position_events_size_pct=10,
        color_events_size_pct=8,
        fire_events_size_pct=0,
    )

    for _ in range(1_000):
        empty_drone_px4.add_fire(0, 0, 0)
    assert get_dance_size_information(empty_drone_px4) == DanceSizeInformation(
        drone_index=0,
        dance_size=24_034,
        position_events_size_pct=10,
        color_events_size_pct=8,
        fire_events_size_pct=6,
    )
