from typing import List, Tuple

from ....parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ....parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from ....show_px4.drone_px4.events.color_events import ColorEvents
from ....show_px4.drone_px4.events.fire_events import FireEvents
from ....show_px4.drone_px4.events.position_events import PositionEvents
from .events_format_check_report import *


def check_int_size_list(elements: List, size_min: int, size_max: int) -> bool:
    return all(size_min <= element and element <= size_max for element in elements)


def check_int_size_list_tuple(
    elements: List[Tuple], size_min: int, size_max: int
) -> bool:
    return all(
        size_min <= element and element <= size_max
        for tuple_element in elements
        for element in tuple_element
    )


def check_frame_rate(
    frames: List[int],
    frame_per_second: int,
    absolute_fps: int,
) -> bool:
    frame_rate = int(absolute_fps // frame_per_second)
    return all(not (frame % frame_rate) for frame in frames)


def check_increasing_frame(frames: List[int]) -> bool:
    return all(
        frames[frame_index] < frames[frame_index + 1]
        for frame_index in range(len(frames) - 1)
    )


def position_frame_check(
    position_events: PositionEvents,
    frame_check_report: FrameCheckReport,
) -> None:
    frames = [event.frame for event in position_events.events]
    frame_check_report.frame_value_check_report.validation = check_int_size_list(
        frames,
        FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
            JSON_BINARY_PARAMETER.show_duration_min_second
        ),
        FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
            JSON_BINARY_PARAMETER.show_duration_max_second
        ),
    )
    frame_check_report.increasing_frame_check_report.validation = (
        check_increasing_frame(frames)
    )
    frame_check_report.update_contenor_validation()


def color_frame_check(
    color_events: ColorEvents,
    frame_check_report: FrameCheckReport,
) -> None:
    frames = [event.frame for event in color_events.events]
    frame_check_report.frame_value_check_report.validation = check_int_size_list(
        frames,
        FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
            JSON_BINARY_PARAMETER.show_duration_min_second
        ),
        FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
            JSON_BINARY_PARAMETER.show_duration_max_second
        ),
    )
    frame_check_report.increasing_frame_check_report.validation = (
        check_increasing_frame(frames)
    )
    frame_check_report.update_contenor_validation()


def xyz_check(
    position_events: PositionEvents,
    xyz_check_report: XyzCheckReport,
) -> None:
    positions = [event.xyz for event in position_events.events]
    # TODO: adapt to the user format
    xyz_check_report.xyz_value_check_report.validation = check_int_size_list_tuple(
        positions,
        JSON_BINARY_PARAMETER.position_value_min,
        JSON_BINARY_PARAMETER.position_value_max,
    )
    xyz_check_report.update_contenor_validation()


def rgbw_check(
    color_events: ColorEvents,
    rgbw_check_report: RgbwCheckReport,
) -> None:
    colors = [event.rgbw for event in color_events.events]
    rgbw_check_report.rgbw_value_check_report.validation = check_int_size_list_tuple(
        colors,
        JSON_BINARY_PARAMETER.color_value_min,
        JSON_BINARY_PARAMETER.color_value_max,
    )
    rgbw_check_report.update_contenor_validation()


def fire_frame_check(
    fire_events: FireEvents,
    fire_events_frame_check_report: FrameCheckReport,
) -> None:
    frames = [event.frame for event in fire_events.events]
    fire_events_frame_check_report.frame_value_check_report.validation = (
        check_int_size_list(
            frames,
            FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
                JSON_BINARY_PARAMETER.show_duration_min_second
            ),
            FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
                JSON_BINARY_PARAMETER.show_duration_max_second
            ),
        )
    )
    fire_events_frame_check_report.update_contenor_validation()


def check_chanel_unicity(chanels: List[int]) -> bool:
    return len(set(chanels)) == len(chanels)


def fire_chanel_check(
    fire_events: FireEvents,
    fire_events_chanel_check_report: FireChanelCheckReport,
) -> None:
    chanels = [event.chanel for event in fire_events.events]
    fire_events_chanel_check_report.fire_chanel_value_check_report.validation = (
        check_int_size_list(
            chanels,
            JSON_BINARY_PARAMETER.fire_chanel_value_min,
            JSON_BINARY_PARAMETER.fire_chanel_value_max,
        )
    )
    fire_events_chanel_check_report.fire_chanel_unicty_check_report.validation = (
        check_chanel_unicity(chanels)
    )
    fire_events_chanel_check_report.update_contenor_validation()


def fire_duration_frame_check(
    fire_events: FireEvents,
    fire_events_chanel_check_report: FireDurationCheckReport,
) -> None:
    durations = [event.duration for event in fire_events.events]
    fire_events_chanel_check_report.fire_duration_value_check_report.validation = (
        check_int_size_list(
            durations,
            JSON_BINARY_PARAMETER.fire_duration_value_frame_min,
            JSON_BINARY_PARAMETER.fire_duration_value_frame_max,
        )
    )
    fire_events_chanel_check_report.update_contenor_validation()
