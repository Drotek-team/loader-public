from typing import List, Tuple

from ....drones_px4.drone_px4.events.color_events import ColorEvents
from ....drones_px4.drone_px4.events.fire_events import FireEvents
from ....drones_px4.drone_px4.events.position_events import PositionEvents
from ....parameter.parameter import (
    IostarParameter,
    FrameParameter,
)
from .events_format_check_report import (
    FireChanelCheckReport,
    FireDurationCheckReport,
    FireTimecodeCheckReport,
    RgbwCheckReport,
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


def check_frame_rate(
    frames: List[int],
    frame_per_second: int,
    json_fps: int,
) -> bool:
    frame_rate = int(json_fps // frame_per_second)
    return all(not (frame % frame_rate) for frame in frames)


def check_increasing_frame(frames: List[int]) -> bool:
    return all(
        frames[frame_index] < frames[frame_index + 1]
        for frame_index in range(len(frames) - 1)
    )


def position_frame_check(
    position_events: PositionEvents,
    frame_check_report: TimecodeCheckReport,
    frame_parameter: FrameParameter,
) -> None:
    frames = [event.frame for event in position_events.events]
    frame_check_report.frame_format_check_report.validation = (
        check_is_instance_int_list(frames)
    )
    frame_check_report.frame_value_check_report.validation = check_int_size_list(
        frames,
        frame_parameter.show_duration_min_frame,
        frame_parameter.show_duration_max_frame,
    )
    frame_check_report.frame_rate_check_report.validation = check_frame_rate(
        frames, frame_parameter.position_fps, frame_parameter.json_fps
    )
    frame_check_report.increasing_frame_check_report.validation = (
        check_increasing_frame(frames)
    )
    frame_check_report.update()


def color_frame_check(
    color_events: ColorEvents,
    frame_check_report: TimecodeCheckReport,
    frame_parameter: FrameParameter,
) -> None:
    frames = [event.frame for event in color_events.events]
    frame_check_report.frame_format_check_report.validation = (
        check_is_instance_int_list(frames)
    )
    frame_check_report.frame_value_check_report.validation = check_int_size_list(
        frames,
        frame_parameter.show_duration_min_frame,
        frame_parameter.show_duration_max_frame,
    )
    frame_check_report.frame_rate_check_report.validation = check_frame_rate(
        frames,
        frame_parameter.color_fps,
        frame_parameter.json_fps,
    )
    frame_check_report.increasing_frame_check_report.validation = (
        check_increasing_frame(frames)
    )
    frame_check_report.update()


### TO DO: clean this typing thing
def xyz_check(
    position_events: PositionEvents,
    xyz_check_report: XyzCheckReport,
    iostar_parameter: IostarParameter,
) -> None:
    positions = [event.xyz for event in position_events.events]
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
    colors = [event.rgbw for event in color_events.events]
    rgbw_check_report.rgbw_format_check_report.validation = (
        check_is_instance_int_list_tuple(colors)
    )
    rgbw_check_report.rgbw_value_check_report.validation = check_int_size_list_tuple(
        colors,
        iostar_parameter.color_value_min,
        iostar_parameter.color_value_max,
    )
    rgbw_check_report.update()


# def takeoff_check(
#     position_events: PositionEvents,
#     takeoff_parameter: TakeoffParameter,
#     frame_parameter: FrameParameter,
#     takeoff_check_report: TakeoffCheckReport,
# ) -> None:
#     if position_events.nb_events == 0:
#         takeoff_check_report.takeoff_duration_check_report.validation = False
#         takeoff_check_report.takeoff_position_check_report.validation = False
#     if position_events.nb_events == 1:
#         first_frame = position_events.get_frame_by_event_index(0)
#         first_position = position_events.get_xyz_by_event_index(0)
#         takeoff_check_report.takeoff_duration_check_report.validation = (
#             takeoff_check_report.takeoff_position_check_report.validation
#         ) = (first_frame == 0)
#         takeoff_check_report.takeoff_position_check_report.validation = (
#             first_position[2] == 0
#         )
#     if position_events.nb_events > 1:
#         first_frame = position_events.get_frame_by_event_index(0)
#         second_frame = position_events.get_frame_by_event_index(1)
#         first_position = position_events.get_xyz_by_event_index(0)
#         second_position = position_events.get_xyz_by_event_index(1)
#         takeoff_check_report.takeoff_duration_check_report.validation = (
#             second_frame - first_frame
#         ) == int(frame_parameter.json_fps * takeoff_parameter.takeoff_duration_second)
#         takeoff_check_report.takeoff_position_check_report.validation = True
#         # takeoff_check_report.takeoff_position_check_report.validation = (
#         #     first_position[0] == second_position[0]
#         #     and first_position[1] == second_position[1]
#         #     and -int(
#         #         json_convertion_constant.METER_TO_CENTIMETER_RATIO
#         #         * takeoff_parameter.takeoff_altitude_meter
#         #     )
#         #     + first_position[2]
#         #     == second_position[2]
#         # )
#     takeoff_check_report.update()


def fire_frame_check(
    fire_events: FireEvents,
    fire_events_frame_check_report: FireTimecodeCheckReport,
    frame_parameter: FrameParameter,
) -> None:
    frames = [event.frame for event in fire_events.events]
    fire_events_frame_check_report.frame_format_check_report.validation = (
        check_is_instance_int_list(frames)
    )
    fire_events_frame_check_report.frame_value_check_report.validation = (
        check_int_size_list(
            frames,
            frame_parameter.show_duration_min_frame,
            frame_parameter.show_duration_max_frame,
        )
    )
    fire_events_frame_check_report.increasing_frame_check_report.validation = (
        check_increasing_frame(frames)
    )
    fire_events_frame_check_report.update()


def check_chanel_unicity(chanels: List[int]) -> bool:
    return len(set(chanels)) == len(chanels)


def fire_chanel_check(
    fire_events: FireEvents,
    fire_events_chanel_check_report: FireChanelCheckReport,
    iostar_parameter: IostarParameter,
) -> None:
    chanels = [event.chanel for event in fire_events.events]
    fire_events_chanel_check_report.fire_chanel_format_check_report.validation = (
        check_is_instance_int_list(chanels)
    )
    fire_events_chanel_check_report.fire_chanel_value_check_report.validation = (
        check_int_size_list(
            chanels,
            iostar_parameter.fire_chanel_value_min,
            iostar_parameter.fire_chanel_value_max,
        )
    )
    fire_events_chanel_check_report.fire_chanel_unicty_check_report.validation = (
        check_chanel_unicity(chanels)
    )
    fire_events_chanel_check_report.update()


def fire_duration_frame_check(
    fire_events: FireEvents,
    fire_events_chanel_check_report: FireDurationCheckReport,
    iostar_parameter: IostarParameter,
) -> None:
    durations = [event.duration for event in fire_events.events]
    fire_events_chanel_check_report.fire_duration_format_check_report.validation = (
        check_is_instance_int_list(durations)
    )
    fire_events_chanel_check_report.fire_duration_value_check_report.validation = (
        check_int_size_list(
            durations,
            iostar_parameter.fire_duration_value_frame_min,
            iostar_parameter.fire_duration_value_frame_max,
        )
    )
    fire_events_chanel_check_report.update()
