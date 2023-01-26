from typing import Any, List

from ....parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from ....report import Contenor, Displayer
from ....show_env.show_px4.drone_px4.events.color_events import ColorEvents
from ....show_env.show_px4.drone_px4.events.events import Events
from ....show_env.show_px4.drone_px4.events.fire_events import FireEvents
from ....show_env.show_px4.drone_px4.events.position_events import PositionEvents


def check_int_size_list(elements: List[Any], size_min: int, size_max: int) -> bool:
    return all(size_min <= element and element <= size_max for element in elements)


def check_int_size_list_tuple(
    elements: List[List[Any]], size_min: int, size_max: int
) -> bool:
    return all(
        size_min <= element and element <= size_max
        for tuple_element in elements
        for element in tuple_element
    )


def check_increasing_frame(frames: List[int]) -> bool:
    return all(
        frames[frame_index] < frames[frame_index + 1]
        for frame_index in range(len(frames) - 1)
    )


# TODO: check frame by frame
def frame_value_check(
    events: Events,
):
    value_displayer = Displayer("Value")
    frames = [event.timecode for event in events]

    if check_int_size_list(
        frames,
        JSON_BINARY_PARAMETER.timecode_value_bound.minimal,
        JSON_BINARY_PARAMETER.timecode_value_bound.maximal,
    ):
        value_displayer.validate()
    return value_displayer


def increasing_frame_check(
    events: Events,
) -> Displayer:
    increasing_displayer = Displayer("Increasing")
    frames = [event.timecode for event in events]
    if check_increasing_frame(frames):
        increasing_displayer.validate()
    return increasing_displayer


def frame_check(
    events: Events,
) -> Contenor:
    frame_check = Contenor("Frame check")
    frame_check.add_error_message(frame_value_check(events))
    frame_check.add_error_message(increasing_frame_check(events))
    return frame_check


def xyz_check(
    position_events: PositionEvents,
) -> Displayer:
    xyz_value_displayer = Displayer("XYZ value check")
    if check_int_size_list_tuple(
        [list(event.xyz) for event in position_events.specific_events],
        JSON_BINARY_PARAMETER.coordinate_value_bound.minimal,
        JSON_BINARY_PARAMETER.coordinate_value_bound.maximal,
    ):
        xyz_value_displayer.validate()
    return xyz_value_displayer


def rgbw_check(
    color_events: ColorEvents,
) -> Displayer:
    rgbw_value_displayer = Displayer("RGBW value check")
    if check_int_size_list_tuple(
        [list(event.rgbw) for event in color_events.specific_events],
        JSON_BINARY_PARAMETER.chrome_value_bound.minimal,
        JSON_BINARY_PARAMETER.chrome_value_bound.maximal,
    ):
        rgbw_value_displayer.validate()
    return rgbw_value_displayer


def fire_chanel_check(
    fire_events: FireEvents,
) -> Displayer:
    fire_chanel_value_displayer = Displayer("Fire chanel value check")
    if check_int_size_list(
        [event.chanel for event in fire_events.specific_events],
        JSON_BINARY_PARAMETER.fire_chanel_value_bound.minimal,
        JSON_BINARY_PARAMETER.fire_chanel_value_bound.maximal,
    ):
        fire_chanel_value_displayer.validate()
    return fire_chanel_value_displayer


def fire_duration_frame_check(
    fire_events: FireEvents,
) -> Displayer:
    fire_duration_value_displayer = Displayer("Fire duration value check")
    durations = [event.duration for event in fire_events.specific_events]
    if check_int_size_list(
        durations,
        JSON_BINARY_PARAMETER.fire_duration_value_bound.minimal,
        JSON_BINARY_PARAMETER.fire_duration_value_bound.maximal,
    ):
        fire_duration_value_displayer.validate()
    return fire_duration_value_displayer
