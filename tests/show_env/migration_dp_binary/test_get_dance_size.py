import struct

from loader.show_env.migration_dp_binary.drone_encoding import get_dance_size
from loader.show_env.show_px4.drone_px4 import (
    DronePx4,
)
from loader.show_env.show_px4.drone_px4.events import (
    ColorEvents,
    FireEvents,
    PositionEvents,
)

DANCE_BASIC_SIZE = 34
POSITION_EVENT_SIZE = struct.calcsize(PositionEvents().format_)
COLOR_EVENT_SIZE = struct.calcsize(ColorEvents().format_)
FIRE_EVENT_SIZE = struct.calcsize(FireEvents().format_)


def test_get_dance_size() -> None:
    empty_drone_px4 = DronePx4(0)
    assert get_dance_size(empty_drone_px4) == DANCE_BASIC_SIZE
    empty_drone_px4.add_position(0, (0, 0, 0))
    assert get_dance_size(empty_drone_px4) == DANCE_BASIC_SIZE + POSITION_EVENT_SIZE
    empty_drone_px4.add_position(0, (0, 0, 0))
    assert get_dance_size(empty_drone_px4) == DANCE_BASIC_SIZE + 2 * POSITION_EVENT_SIZE
    empty_drone_px4.add_color(0, (0, 0, 0, 0))
    assert (
        get_dance_size(empty_drone_px4)
        == DANCE_BASIC_SIZE + 2 * POSITION_EVENT_SIZE + COLOR_EVENT_SIZE
    )
    empty_drone_px4.add_fire(0, 0, 0)
    assert (
        get_dance_size(empty_drone_px4)
        == DANCE_BASIC_SIZE
        + 2 * POSITION_EVENT_SIZE
        + COLOR_EVENT_SIZE
        + FIRE_EVENT_SIZE
    )
