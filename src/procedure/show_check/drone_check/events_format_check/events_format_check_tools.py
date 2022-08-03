from typing import List, Tuple

from .....drones_manager.drone.events.color_events import ColorEvents
from .....drones_manager.drone.events.fire_events import FireEvents
from .....drones_manager.drone.events.position_events import PositionEvents
from .....parameter.parameter import (
    IostarParameter,
    TakeoffParameter,
    TimecodeParameter,
)
from .events_format_check_report import (
    FireChanelCheckReport,
    FireDurationCheckReport,
    FireTimecodeCheckReport,
    RgbwCheckReport,
    TakeoffCheckReport,
    TimecodeCheckReport,
    XyzCheckReport,
)


def check_is_instance_int_list(elements: List) -> bool:
    return all(isinstance(element, int) for element in elements)


def check_is_instance_int_list_tuple(elements: List[Tuple]) -> bool:
    return all(
        isinstance(element, int)
        for element_tuple in elements
        for element in element_tuple
    )


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


def check_timecode_rate(timecodes: List[int], timecode_rate: int) -> bool:
    return all(
        second_timecode - first_timecode >= timecode_rate
        for first_timecode, second_timecode in zip(timecodes[:-2], timecodes[2:])
    )


def check_increasing_timecode(timecodes: List[int]) -> bool:
    return all(
        timecodes[timecode_index] < timecodes[timecode_index + 1]
        for timecode_index in range(len(timecodes) - 1)
    )


def position_timecode_check(
    position_events: PositionEvents,
    timecode_check_report: TimecodeCheckReport,
    timecode_parameter: TimecodeParameter,
) -> None:
    timecodes = [event.timecode for event in position_events.event_list]
    timecode_check_report.timecode_format_check_report.validation = (
        check_is_instance_int_list(timecodes)
    )
    timecode_check_report.timecode_value_check_report.validation = check_int_size_list(
        timecodes,
        timecode_parameter.show_timecode_begin,
        timecode_parameter.timecode_value_max,
    )
    timecode_check_report.timecode_rate_check_report.validation = check_timecode_rate(
        timecodes, timecode_parameter.position_timecode_rate
    )
    timecode_check_report.increasing_timecode_check_report.validation = (
        check_increasing_timecode(timecodes)
    )
    timecode_check_report.update()


def color_timecode_check(
    color_events: ColorEvents,
    timecode_check_report: TimecodeCheckReport,
    timecode_parameter: TimecodeParameter,
) -> None:
    timecodes = [event.timecode for event in color_events.event_list]
    timecode_check_report.timecode_format_check_report.validation = (
        check_is_instance_int_list(timecodes)
    )
    timecode_check_report.timecode_value_check_report.validation = check_int_size_list(
        timecodes,
        timecode_parameter.show_timecode_begin,
        timecode_parameter.timecode_value_max,
    )
    timecode_check_report.timecode_rate_check_report.validation = check_timecode_rate(
        timecodes, timecode_parameter.color_timecode_rate
    )
    timecode_check_report.increasing_timecode_check_report.validation = (
        check_increasing_timecode(timecodes)
    )
    timecode_check_report.update()


def xyz_check(
    position_events: PositionEvents,
    xyz_check_report: XyzCheckReport,
    iostar_parameter: IostarParameter,
) -> None:
    positions = [event.get_values() for event in position_events.events]
    xyz_check_report.xyz_format_check_report.validation = (
        check_is_instance_int_list_tuple(positions)
    )
    xyz_check_report.xyz_value_check_report.validation = check_int_size_list_tuple(
        positions,
        iostar_parameter.position_value_min,
        iostar_parameter.position_value_max,
    )
    xyz_check_report.update()


def rgbw_check(
    color_events: ColorEvents,
    rgbw_check_report: RgbwCheckReport,
    iostar_parameter: IostarParameter,
) -> None:
    colors = [event.get_values() for event in color_events.events]
    rgbw_check_report.rgbw_format_check_report.validation = (
        check_is_instance_int_list_tuple(colors)
    )
    rgbw_check_report.rgbw_value_check_report.validation = check_int_size_list_tuple(
        colors,
        iostar_parameter.color_value_min,
        iostar_parameter.color_value_max,
    )
    rgbw_check_report.update()


def takeoff_check(
    position_events: PositionEvents,
    takeoff_check_report: TakeoffCheckReport,
    takeoff_parameter: TakeoffParameter,
) -> None:

    if position_events.nb_events == 0:
        takeoff_check_report.takeoff_duration_check_report.validation = False
        takeoff_check_report.takeoff_position_check_report.validation = False
    if position_events.nb_events == 1:
        first_timecode = position_events.get_timecode_by_event_index(0)
        first_position = position_events.get_values_by_event_index(0)
        takeoff_check_report.takeoff_duration_check_report.validation = (
            takeoff_check_report.takeoff_position_check_report.validation
        ) = (first_timecode == 0)
        takeoff_check_report.takeoff_position_check_report.validation = (
            first_position[2] == 0
        )
    if position_events.nb_events > 1:
        first_timecode = position_events.get_timecode_by_event_index(0)
        second_timecode = position_events.get_timecode_by_event_index(1)
        first_position = position_events.get_values_by_event_index(0)
        second_position = position_events.get_values_by_event_index(1)
        takeoff_check_report.takeoff_duration_check_report.validation = (
            second_timecode - first_timecode
        ) == takeoff_parameter.takeoff_duration
        takeoff_check_report.takeoff_position_check_report.validation = True
        takeoff_check_report.takeoff_position_check_report.validation = (
            first_position[0] == second_position[0]
            and first_position[1] == second_position[1]
            and -takeoff_parameter.takeoff_altitude + first_position[2]
            == second_position[2]
        )
    takeoff_check_report.update()


def fire_timecode_check(
    fire_events: ColorEvents,
    fire_events_timecode_check_report: FireTimecodeCheckReport,
    timecode_parameter: TimecodeParameter,
) -> None:
    timecodes = [event.timecode for event in fire_events.event_list]
    fire_events_timecode_check_report.timecode_format_check_report.validation = (
        check_is_instance_int_list(timecodes)
    )
    fire_events_timecode_check_report.timecode_value_check_report.validation = (
        check_int_size_list(
            timecodes,
            timecode_parameter.show_timecode_begin,
            timecode_parameter.timecode_value_max,
        )
    )
    fire_events_timecode_check_report.increasing_timecode_check_report.validation = (
        check_increasing_timecode(timecodes)
    )
    fire_events_timecode_check_report.update()


def check_chanel_unicity(chanels: List[int]) -> bool:
    return len(set(chanels)) == len(chanels)


def fire_chanel_check(
    fire_events: FireEvents,
    fire_events_chanel_check_report: FireChanelCheckReport,
    iostar_parameter: IostarParameter,
) -> None:
    channels = [event.get_values()[0] for event in fire_events.event_list]
    fire_events_chanel_check_report.fire_chanel_format_check_report.validation = (
        check_is_instance_int_list(channels)
    )
    fire_events_chanel_check_report.fire_chanel_value_check_report.validation = (
        check_int_size_list(
            channels,
            iostar_parameter.fire_chanel_value_min,
            iostar_parameter.fire_chanel_value_max,
        )
    )
    fire_events_chanel_check_report.fire_chanel_unicty_check_report.validation = (
        check_chanel_unicity(channels)
    )
    fire_events_chanel_check_report.update()


def fire_duration_check(
    fire_events: FireEvents,
    fire_events_chanel_check_report: FireDurationCheckReport,
    iostar_parameter: IostarParameter,
) -> None:
    durations = [event.get_values()[1] for event in fire_events.event_list]
    fire_events_chanel_check_report.fire_duration_format_check_report.validation = (
        check_is_instance_int_list(durations)
    )
    fire_events_chanel_check_report.fire_duration_value_check_report.validation = (
        check_int_size_list(
            durations,
            iostar_parameter.fire_duration_value_min,
            iostar_parameter.fire_duration_value_max,
        )
    )
    fire_events_chanel_check_report.update()
