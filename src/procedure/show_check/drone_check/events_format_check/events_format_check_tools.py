from typing import Any, List, Tuple

from .....drones_manager.drone.events.position_events import PositionEvents
from .....parameter.parameter import (
    IostarParameter,
    TakeoffParameter,
    TimecodeParameter,
)
from .events_format_check_report import (
    TakeoffCheckReport,
    TimecodeCheckReport,
    XyzCheckReport,
)


def check_int(elements: List[Any]) -> bool:
    return all(isinstance(element, int) for element in elements)


def check_int_size(elements: Tuple, size_min: int, size_max: int) -> bool:
    return all(size_min < element and element < size_max for element in elements)


def check_timecode_rate(timecodes: List[int], timecode_rate: int) -> bool:
    return all(not (timecode % timecode_rate) for timecode in timecodes)


def check_increasing_timecode(timecodes: List[int]) -> bool:
    return all(
        timecodes[timecode_index] < timecodes[timecode_index + 1]
        for timecode_index in range(len(timecodes) - 1)
    )


def check_first_timecode(timecodes: List[int], minimal_timecode: int) -> bool:
    return timecodes[0] >= minimal_timecode


def timecode_check(
    position_events: PositionEvents,
    timecode_check_report: TimecodeCheckReport,
    timecode_parameter: TimecodeParameter,
) -> None:
    timecodes = [event.timecode for event in position_events.event_list]
    timecode_check_report.timecode_format_check_report.validation = check_int(timecodes)
    timecode_check_report.timecode_rate_check_report.validation = check_timecode_rate(
        timecodes, timecode_parameter.position_rate
    )
    timecode_check_report.increasing_timecode_check_report.validation = (
        check_increasing_timecode(timecodes)
    )
    timecode_check_report.first_timecode_check_report.validation = check_first_timecode(
        timecodes, timecode_parameter.show_timecode_begin
    )
    timecode_check_report.update()


def xyz_check(
    position_events: PositionEvents,
    xyz_check_report: XyzCheckReport,
    iostar_parameter: IostarParameter,
) -> None:
    positions = [event.get_values() for event in position_events.events]
    xyz_check_report.validation = all(
        check_int_size(
            xyz,
            iostar_parameter.position_format_min,
            iostar_parameter.position_format_max,
        )
        for xyz in positions
    )


def rgbw_check(
    positions: List[Tuple[int, int, int, int]], iostar_parameter: IostarParameter
) -> None:
    all(
        check_int_size(
            xyz, iostar_parameter.color_format_min, iostar_parameter.color_format_max
        )
        for xyz in positions
    )


def fire_chanel_check(
    fire_chanels: List[int], iostar_parameter: IostarParameter
) -> None:
    all(
        check_int_size(
            tuple([fire_chanel]),
            iostar_parameter.fire_chanel_format_min,
            iostar_parameter.fire_chanel_format_max,
        )
        for fire_chanel in fire_chanels
    )


def fire_duration_check(
    fire_durations: List[int], iostar_parameter: IostarParameter
) -> None:
    all(
        check_int_size(
            tuple([fire_duration]),
            iostar_parameter.fire_duration_format_min,
            iostar_parameter.fire_duration_format_max,
        )
        for fire_duration in fire_durations
    )


def takeoff_check(
    position_events: PositionEvents,
    takeoff_check_report: TakeoffCheckReport,
    takeoff_parameter: TakeoffParameter,
) -> None:
    first_timecode = position_events.get_timecode_by_event_index(0)
    second_timecode = position_events.get_timecode_by_event_index(1)
    first_position = position_events.get_values_by_event_index(0)
    second_position = position_events.get_values_by_event_index(1)
    standard_takeoff_duration = (
        second_timecode - first_timecode
    ) == takeoff_parameter.takeoff_duration
    standard_takeoff_translation = (
        first_position[0] == second_position[0]
        and first_position[1] == second_position[1]
        and takeoff_parameter.takeoff_altitude + first_position[2] == second_position[2]
    )
    takeoff_check_report.validation = (
        standard_takeoff_duration and standard_takeoff_translation
    )
