import struct

from src.migration.show_px4.drone_px4.drone_px4 import *

from .drone_encoding_procedure import get_dance_size

DANCE_BASIC_SIZE = 34
POSITION_EVENT_SIZE = struct.calcsize(PositionEvents.format_)
COLOR_EVENT_SIZE = struct.calcsize(ColorEvents.format_)
FIRE_EVENT_SIZE = struct.calcsize(FireEvents.format_)


def test_get_dance_size():
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
