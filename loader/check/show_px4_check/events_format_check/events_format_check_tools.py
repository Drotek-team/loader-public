from typing import List, Tuple

from loader.parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from loader.report.report import Contenor, Displayer
from loader.show_env.show_px4.drone_px4.events.color_events import ColorEvents
from loader.show_env.show_px4.drone_px4.events.events import Events
from loader.show_env.show_px4.drone_px4.events.fire_events import FireEvents
from loader.show_env.show_px4.drone_px4.events.position_events import PositionEvents


def check_integer_bound(integer: int, lower_bound: int, upper_bound: int) -> bool:
    return lower_bound <= integer and integer <= upper_bound


def check_increasing_frame(frames: List[int]) -> bool:
    return all(
        frames[frame_index] < frames[frame_index + 1]
        for frame_index in range(len(frames) - 1)
    )


def timecodes_value_check(
    events: Events,
) -> Contenor:
    value_contenor = Contenor("Values")
    for frame_index, frame in enumerate([event.timecode for event in events]):
        if not (
            check_integer_bound(
                frame,
                JSON_BINARY_PARAMETER.timecode_value_bound.minimal,
                JSON_BINARY_PARAMETER.timecode_value_bound.maximal,
            )
        ):
            value_contenor.add_error_message(
                Displayer(
                    f"{frame} at the index {frame_index} is not in the bound"
                    f"{JSON_BINARY_PARAMETER.timecode_value_bound.minimal}"
                    f"to {JSON_BINARY_PARAMETER.timecode_value_bound.maximal}",
                ),
            )
    return value_contenor


def increasing_timecode_check(
    events: Events,
) -> Displayer:
    increasing_displayer = Displayer("Increasing")
    frames = [event.timecode for event in events]
    if check_increasing_frame(frames):
        increasing_displayer.validate()
    return increasing_displayer


def timecodes_check(
    events: Events,
) -> Contenor:
    frame_check = Contenor("Frame check")
    frame_check.add_error_message(timecodes_value_check(events))
    frame_check.add_error_message(increasing_timecode_check(events))
    return frame_check


def coordinate_value_check(frame_index: int, xyz: Tuple[int, int, int]) -> Contenor:
    coordinate_value_contenor = Contenor(
        f"Coordinate value at frame index {frame_index}",
    )
    for coordinate_index in range(3):
        if not (
            check_integer_bound(
                xyz[coordinate_index],
                JSON_BINARY_PARAMETER.coordinate_value_bound.minimal,
                JSON_BINARY_PARAMETER.coordinate_value_bound.maximal,
            )
        ):
            coordinate_value_contenor.add_error_message(
                Displayer(
                    f"{xyz[coordinate_index]} at the coordinate {coordinate_index}"
                    f"is not in the bound"
                    f"{JSON_BINARY_PARAMETER.coordinate_value_bound.minimal}"
                    f"to {JSON_BINARY_PARAMETER.coordinate_value_bound.maximal}",
                ),
            )
    return coordinate_value_contenor


def coordinates_value_check(
    position_events: PositionEvents,
) -> Contenor:
    value_contenor = Contenor("Values")
    for position_event_index, position_event in enumerate(
        position_events.specific_events,
    ):
        value_contenor.add_error_message(
            coordinate_value_check(
                position_event_index,
                position_event.xyz,
            ),
        )
    return value_contenor


def chrome_value_check(frame_index: int, rgbw: Tuple[int, int, int, int]) -> Contenor:
    coordinate_value_contenor = Contenor(f"Chrome value at frame index {frame_index}")
    for chrome_index in range(4):
        if not (
            check_integer_bound(
                rgbw[chrome_index],
                JSON_BINARY_PARAMETER.chrome_value_bound.minimal,
                JSON_BINARY_PARAMETER.chrome_value_bound.maximal,
            )
        ):
            coordinate_value_contenor.add_error_message(
                Displayer(
                    f"{rgbw[chrome_index]} at the coordinate {chrome_index}"
                    f"is not in the bound"
                    f"{JSON_BINARY_PARAMETER.chrome_value_bound.minimal}"
                    f"to {JSON_BINARY_PARAMETER.chrome_value_bound.maximal}",
                ),
            )
    return coordinate_value_contenor


def chromes_value_check(
    color_events: ColorEvents,
) -> Contenor:
    value_contenor = Contenor("Values")
    for color_event_index, color_event in enumerate(color_events.specific_events):
        value_contenor.add_error_message(
            chrome_value_check(
                color_event_index,
                color_event.rgbw,
            ),
        )
    return value_contenor


def fire_chanel_duration_check(
    fire_events: FireEvents,
) -> Contenor:
    value_contenor = Contenor("Values")
    for fire_event_index, fire_event in enumerate(fire_events.specific_events):
        if not (
            check_integer_bound(
                fire_event.chanel,
                JSON_BINARY_PARAMETER.fire_chanel_value_bound.minimal,
                JSON_BINARY_PARAMETER.fire_chanel_value_bound.maximal,
            )
        ):
            value_contenor.add_error_message(
                Displayer(
                    f"{fire_event.chanel} chanel at "
                    f"the frame index {fire_event_index} is not in the bound"
                    f"{JSON_BINARY_PARAMETER.fire_chanel_value_bound.minimal}"
                    f"to {JSON_BINARY_PARAMETER.fire_chanel_value_bound.maximal}",
                ),
            )
        if not (
            check_integer_bound(
                fire_event.duration,
                JSON_BINARY_PARAMETER.fire_duration_value_bound.minimal,
                JSON_BINARY_PARAMETER.fire_duration_value_bound.maximal,
            )
        ):
            value_contenor.add_error_message(
                Displayer(
                    f"{fire_event.duration} duration at "
                    f"the frame index {fire_event_index} is not in the bound"
                    f"{JSON_BINARY_PARAMETER.fire_duration_value_bound.minimal}"
                    f"to {JSON_BINARY_PARAMETER.fire_duration_value_bound.maximal}",
                ),
            )
    return value_contenor
