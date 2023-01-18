from typing import Any, List

from ....parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
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


def frame_check(
    events: Events,
) -> Contenor:
    frame_check = Contenor("Frame check")
    value_displayer = Displayer("Value")
    increasing_displayer = Displayer("Increasing")
    frame_check.add_error_message(value_displayer)
    frame_check.add_error_message(increasing_displayer)
    frames = [event.timecode for event in events]
    if check_int_size_list(
        frames,
        FRAME_PARAMETER.from_second_to_frame(
            JSON_BINARY_PARAMETER.show_duration_min_second
        ),
        FRAME_PARAMETER.from_second_to_frame(
            JSON_BINARY_PARAMETER.show_duration_max_second
        ),
    ):
        value_displayer.validate()
    if check_increasing_frame(frames):
        increasing_displayer.validate()
    return frame_check


def xyz_check(
    position_events: PositionEvents,
) -> Contenor:
    xyz_contenor = Contenor("Xyz check")
    value_displayer = Displayer("Value")
    xyz_contenor.add_error_message(value_displayer)
    if check_int_size_list_tuple(
        [list(event.xyz) for event in position_events.specific_events],
        JSON_BINARY_PARAMETER.position_value_min,
        JSON_BINARY_PARAMETER.position_value_max,
    ):
        value_displayer.validate()
    return xyz_contenor


def rgbw_check(
    color_events: ColorEvents,
) -> Contenor:
    rgbw_check = Contenor("Rgbw check")
    value_displayer = Displayer("Value")
    rgbw_check.add_error_message(value_displayer)
    if check_int_size_list_tuple(
        [list(event.rgbw) for event in color_events.specific_events],
        JSON_BINARY_PARAMETER.color_value_min,
        JSON_BINARY_PARAMETER.color_value_max,
    ):
        value_displayer.validate()
    return rgbw_check


def check_chanel_unicity(chanels: List[int]) -> bool:
    return len(set(chanels)) == len(chanels)


def fire_chanel_check(
    fire_events: FireEvents,
) -> Contenor:
    fire_chanel_contenor = Contenor("Fire chanel check")
    value_displayer = Displayer("Value")
    fire_chanel_contenor.add_error_message(value_displayer)
    if check_int_size_list(
        [event.chanel for event in fire_events.specific_events],
        JSON_BINARY_PARAMETER.fire_chanel_value_min,
        JSON_BINARY_PARAMETER.fire_chanel_value_max,
    ):
        value_displayer.validate()
    return fire_chanel_contenor


def fire_duration_frame_check(
    fire_events: FireEvents,
) -> Contenor:
    fire_chanel_contenor = Contenor("Fire duration check")
    value_displayer = Displayer("Value")
    fire_chanel_contenor.add_error_message(value_displayer)
    durations = [event.duration for event in fire_events.specific_events]
    if check_int_size_list(
        durations,
        JSON_BINARY_PARAMETER.fire_duration_value_frame_min,
        JSON_BINARY_PARAMETER.fire_duration_value_frame_max,
    ):
        value_displayer.validate()
    return fire_chanel_contenor
    return fire_chanel_contenor
