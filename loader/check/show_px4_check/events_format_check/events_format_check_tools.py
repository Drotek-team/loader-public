from typing import List, Optional

from loader.parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from loader.report.report import BaseInfraction, BaseReport
from loader.show_env.show_px4.drone_px4.events.color_events import ColorEvents
from loader.show_env.show_px4.drone_px4.events.events import Events
from loader.show_env.show_px4.drone_px4.events.fire_events import FireEvents
from loader.show_env.show_px4.drone_px4.events.position_events import PositionEvents


class IntegerBoundaryInfraction(BaseInfraction):
    data_type: str
    event_index: int
    value: int
    value_min: int
    value_max: int


class IncreasingFrameInfraction(BaseInfraction):
    event_index: int
    previous_frame: int
    frame: int


def check_integer_bound(integer: int, lower_bound: int, upper_bound: int) -> bool:
    return lower_bound <= integer and integer <= upper_bound


def get_timecode_value_infractions(
    events: Events,
) -> List[IntegerBoundaryInfraction]:
    return [
        IntegerBoundaryInfraction(
            data_type="frame",
            event_index=event_index,
            value=frame,
            value_min=JSON_BINARY_PARAMETER.timecode_value_bound.minimal,
            value_max=JSON_BINARY_PARAMETER.timecode_value_bound.maximal,
        )
        for event_index, frame in enumerate([event.timecode for event in events])
        if not (
            check_integer_bound(
                frame,
                JSON_BINARY_PARAMETER.timecode_value_bound.minimal,
                JSON_BINARY_PARAMETER.timecode_value_bound.maximal,
            )
        )
    ]


def get_increasing_timecode_infractions(
    events: Events,
) -> List[IncreasingFrameInfraction]:
    frames = [event.timecode for event in events]
    return [
        IncreasingFrameInfraction(
            event_index=event_index,
            previous_frame=frames[event_index - 1],
            frame=frames[event_index],
        )
        for event_index in range(1, len(frames))
        if frames[event_index - 1] >= frames[event_index]
    ]


class TimecodeReport(BaseReport):
    bound_infractions: List[IntegerBoundaryInfraction] = []
    increasing_infractions: List[IncreasingFrameInfraction] = []


def get_timecode_report(
    events: Events,
) -> Optional[TimecodeReport]:
    bound_infractions = get_timecode_value_infractions(events)
    increasing_infractions = get_increasing_timecode_infractions(events)
    if bound_infractions or increasing_infractions:
        return TimecodeReport(
            bound_infractions=bound_infractions,
            increasing_infractions=increasing_infractions,
        )
    return None


def get_coordinate_infractions(
    position_events: PositionEvents,
) -> List[IntegerBoundaryInfraction]:
    return [
        IntegerBoundaryInfraction(
            data_type="coordinate",
            event_index=event_index,
            value=position_event.xyz[coordinate_index],
            value_min=JSON_BINARY_PARAMETER.coordinate_value_bound.minimal,
            value_max=JSON_BINARY_PARAMETER.coordinate_value_bound.maximal,
        )
        for event_index, position_event in enumerate(
            position_events.specific_events,
        )
        for coordinate_index in range(3)
        if not (
            check_integer_bound(
                position_event.xyz[coordinate_index],
                JSON_BINARY_PARAMETER.coordinate_value_bound.minimal,
                JSON_BINARY_PARAMETER.coordinate_value_bound.maximal,
            )
        )
    ]


def get_chrome_infractions(
    color_events: ColorEvents,
) -> List[IntegerBoundaryInfraction]:
    return [
        IntegerBoundaryInfraction(
            data_type="chrome",
            event_index=event_index,
            value=color_event.rgbw[chrome_index],
            value_min=JSON_BINARY_PARAMETER.chrome_value_bound.minimal,
            value_max=JSON_BINARY_PARAMETER.chrome_value_bound.maximal,
        )
        for event_index, color_event in enumerate(
            color_events.specific_events,
        )
        for chrome_index in range(4)
        if not (
            check_integer_bound(
                color_event.rgbw[chrome_index],
                JSON_BINARY_PARAMETER.chrome_value_bound.minimal,
                JSON_BINARY_PARAMETER.chrome_value_bound.maximal,
            )
        )
    ]


def get_duration_chanel_infractions(
    fire_events: FireEvents,
) -> List[IntegerBoundaryInfraction]:
    fire_duration_boundary_infractions = [
        IntegerBoundaryInfraction(
            data_type="fire duration",
            event_index=event_index,
            value=fire_event.duration,
            value_min=JSON_BINARY_PARAMETER.fire_duration_value_bound.minimal,
            value_max=JSON_BINARY_PARAMETER.fire_duration_value_bound.maximal,
        )
        for event_index, fire_event in enumerate(
            fire_events.specific_events,
        )
        if not (
            check_integer_bound(
                fire_event.duration,
                JSON_BINARY_PARAMETER.fire_duration_value_bound.minimal,
                JSON_BINARY_PARAMETER.fire_duration_value_bound.maximal,
            )
        )
    ]
    fire_chanel_boundary_infractions = [
        IntegerBoundaryInfraction(
            data_type="fire chanel",
            event_index=event_index,
            value=fire_event.chanel,
            value_min=JSON_BINARY_PARAMETER.fire_chanel_value_bound.minimal,
            value_max=JSON_BINARY_PARAMETER.fire_chanel_value_bound.maximal,
        )
        for event_index, fire_event in enumerate(
            fire_events.specific_events,
        )
        if not (
            check_integer_bound(
                fire_event.chanel,
                JSON_BINARY_PARAMETER.fire_chanel_value_bound.minimal,
                JSON_BINARY_PARAMETER.fire_chanel_value_bound.maximal,
            )
        )
    ]
    return fire_duration_boundary_infractions + fire_chanel_boundary_infractions
