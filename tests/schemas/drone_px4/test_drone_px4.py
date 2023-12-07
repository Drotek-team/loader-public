import pytest
from loader.parameters.json_binary_parameters import LandType, MagicNumber
from loader.schemas.drone_px4 import DronePx4
from loader.schemas.drone_px4.events.events_order import EventsType


@pytest.mark.parametrize("magic_number", list(MagicNumber))
def test_add_position_standard_case(magic_number: MagicNumber) -> None:
    drone = DronePx4(index=0, magic_number=magic_number, scale=1, land_type=LandType.Land)
    drone.add_position(frame=0, xyz=(0, 0, 0))
    assert drone.position_events[0].get_data(magic_number) == [0, 0, 0, 0]
    drone.add_position(frame=1, xyz=(1, 1, 1))
    assert drone.position_events[1].get_data(magic_number) == [
        42 if magic_number == MagicNumber.v1 else 1,
        1,
        1,
        1,
    ]


@pytest.mark.parametrize("magic_number", list(MagicNumber))
def test_add_color_standard_case(magic_number: MagicNumber) -> None:
    drone = DronePx4(index=0, magic_number=magic_number, scale=1, land_type=LandType.Land)
    drone.add_color(frame=0, rgbw=(0, 0, 0, 0))
    assert drone.color_events[0].get_data(magic_number) == [0, 0, 0, 0, 0]
    drone.add_color(frame=1, rgbw=(1, 1, 1, 1), interpolate=True)
    assert drone.color_events[1].get_data(magic_number) == [
        42 if magic_number == MagicNumber.v1 else 1,
        1,
        1,
        1,
        1 if magic_number == MagicNumber.v1 else 128,
    ]


@pytest.mark.parametrize("magic_number", list(MagicNumber))
def test_add_fire_standard_case(magic_number: MagicNumber) -> None:
    drone = DronePx4(index=0, magic_number=magic_number, scale=1, land_type=LandType.Land)
    drone.add_fire(frame=0, channel=1, duration=2)
    assert drone.fire_events[0].get_data(magic_number) == [0, 1, 2]
    drone.add_fire(frame=1, channel=3, duration=4)
    assert drone.fire_events[1].get_data(magic_number) == [
        42 if magic_number == MagicNumber.v1 else 1,
        3,
        4,
    ]


@pytest.mark.parametrize("magic_number", list(MagicNumber))
def test_get_events_by_index_standard_case(magic_number: MagicNumber) -> None:
    drone = DronePx4(index=0, magic_number=magic_number, scale=1, land_type=LandType.Land)
    assert drone.get_events_by_index(event_type=EventsType.position) == drone.position_events
    assert drone.get_events_by_index(event_type=EventsType.color) == drone.color_events
    assert drone.get_events_by_index(event_type=EventsType.fire) == drone.fire_events


@pytest.mark.parametrize("magic_number", list(MagicNumber))
def test_events_list_standard_case(magic_number: MagicNumber) -> None:
    drone = DronePx4(index=0, magic_number=magic_number, scale=1, land_type=LandType.Land)
    assert drone.events_dict == {
        EventsType.position: drone.position_events,
        EventsType.color: drone.color_events,
        EventsType.fire: drone.fire_events,
    }


@pytest.mark.parametrize("magic_number", list(MagicNumber))
def test_non_empty_events_list_standard_case(magic_number: MagicNumber) -> None:
    drone = DronePx4(index=0, magic_number=magic_number, scale=1, land_type=LandType.Land)
    assert drone.non_empty_events_list == []
    drone.add_position(frame=0, xyz=(0, 0, 0))
    assert drone.non_empty_events_list == [drone.position_events]
    drone.add_color(frame=0, rgbw=(0, 0, 0, 0))
    assert drone.non_empty_events_list == [drone.position_events, drone.color_events]
    drone.add_fire(frame=0, channel=0, duration=0)
    assert drone.non_empty_events_list == [
        drone.position_events,
        drone.color_events,
        drone.fire_events,
    ]


@pytest.mark.parametrize("magic_number", list(MagicNumber))
def test___eq___standard_case(magic_number: MagicNumber) -> None:
    drone = DronePx4(index=0, magic_number=magic_number, scale=1, land_type=LandType.Land)
    assert drone == drone  # noqa: PLR0124
    other_drone = DronePx4(index=0, magic_number=magic_number, scale=1, land_type=LandType.Land)
    assert drone == other_drone
    drone.add_position(frame=0, xyz=(0, 0, 0))
    assert drone != other_drone
    other_drone.add_position(frame=0, xyz=(0, 0, 0))
    assert drone == other_drone
    drone.add_color(frame=0, rgbw=(0, 0, 0, 0))
    assert drone != other_drone
    other_drone.add_color(frame=0, rgbw=(0, 0, 0, 0))
    assert drone == other_drone
    drone.add_fire(frame=0, channel=0, duration=0)
    assert drone != other_drone
    other_drone.add_fire(frame=0, channel=0, duration=0)
    assert drone == other_drone


@pytest.mark.parametrize("magic_number", list(MagicNumber))
def test___eq___with_other_type(magic_number: MagicNumber) -> None:
    drone = DronePx4(index=0, magic_number=magic_number, scale=1, land_type=LandType.Land)
    assert drone != 0
