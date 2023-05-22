# pyright: reportIncompatibleMethodOverride=false
from typing import List

from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS
from loader.reports.base import BaseInfraction, BaseReport
from loader.schemas.drone_px4.events import (
    ColorEvents,
    Events,
    FireEvents,
    PositionEvents,
)


class IntegerBoundaryInfraction(BaseInfraction):
    event_index: int
    value: int
    value_min: int
    value_max: int


class IncreasingFrameInfraction(BaseInfraction):
    event_index: int
    previous_frame: int
    frame: int

    @classmethod
    def generate(
        cls,
        events: Events,
    ) -> List["IncreasingFrameInfraction"]:
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


def check_integer_bound(integer: int, lower_bound: int, upper_bound: int) -> bool:
    return lower_bound <= integer and integer <= upper_bound


class TimeCodeValueInfraction(IntegerBoundaryInfraction):
    @classmethod
    def generate(
        cls,
        events: Events,
    ) -> List["TimeCodeValueInfraction"]:
        return [
            TimeCodeValueInfraction(
                event_index=event_index,
                value=frame,
                value_min=JSON_BINARY_PARAMETERS.timecode_value_bound.minimal,
                value_max=JSON_BINARY_PARAMETERS.timecode_value_bound.maximal,
            )
            for event_index, frame in enumerate([event.timecode for event in events])
            if not (
                check_integer_bound(
                    frame,
                    JSON_BINARY_PARAMETERS.timecode_value_bound.minimal,
                    JSON_BINARY_PARAMETERS.timecode_value_bound.maximal,
                )
            )
        ]


class TimecodeReport(BaseReport):
    bound_infractions: List[TimeCodeValueInfraction] = []
    increasing_infractions: List[IncreasingFrameInfraction] = []

    @classmethod
    def generate(
        cls,
        events: Events,
    ) -> "TimecodeReport":
        bound_infractions = TimeCodeValueInfraction.generate(events)
        increasing_infractions = IncreasingFrameInfraction.generate(events)
        return TimecodeReport(
            bound_infractions=bound_infractions,
            increasing_infractions=increasing_infractions,
        )


class CoordinateInfraction(IntegerBoundaryInfraction):
    @classmethod
    def generate(
        cls,
        position_events: PositionEvents,
    ) -> List["CoordinateInfraction"]:
        return [
            CoordinateInfraction(
                event_index=event_index,
                value=position_event.xyz[coordinate_index],
                value_min=JSON_BINARY_PARAMETERS.coordinate_value_bound.minimal,
                value_max=JSON_BINARY_PARAMETERS.coordinate_value_bound.maximal,
            )
            for event_index, position_event in enumerate(
                position_events.specific_events,
            )
            for coordinate_index in range(3)
            if not (
                check_integer_bound(
                    position_event.xyz[coordinate_index],
                    JSON_BINARY_PARAMETERS.coordinate_value_bound.minimal,
                    JSON_BINARY_PARAMETERS.coordinate_value_bound.maximal,
                )
            )
        ]


class ChromeInfraction(IntegerBoundaryInfraction):
    @classmethod
    def generate(
        cls,
        color_events: ColorEvents,
    ) -> List["ChromeInfraction"]:
        return [
            ChromeInfraction(
                event_index=event_index,
                value=color_event.rgbw[chrome_index],
                value_min=JSON_BINARY_PARAMETERS.chrome_value_bound.minimal,
                value_max=JSON_BINARY_PARAMETERS.chrome_value_bound.maximal,
            )
            for event_index, color_event in enumerate(
                color_events.specific_events,
            )
            for chrome_index in range(4)
            if not (
                check_integer_bound(
                    color_event.rgbw[chrome_index],
                    JSON_BINARY_PARAMETERS.chrome_value_bound.minimal,
                    JSON_BINARY_PARAMETERS.chrome_value_bound.maximal,
                )
            )
        ]


class DurationChanelInfraction(IntegerBoundaryInfraction):
    @classmethod
    def generate(
        cls,
        fire_events: FireEvents,
    ) -> List["DurationChanelInfraction"]:
        fire_duration_boundary_infractions = [
            DurationChanelInfraction(
                event_index=event_index,
                value=fire_event.duration,
                value_min=JSON_BINARY_PARAMETERS.fire_duration_value_bound.minimal,
                value_max=JSON_BINARY_PARAMETERS.fire_duration_value_bound.maximal,
            )
            for event_index, fire_event in enumerate(
                fire_events.specific_events,
            )
            if not (
                check_integer_bound(
                    fire_event.duration,
                    JSON_BINARY_PARAMETERS.fire_duration_value_bound.minimal,
                    JSON_BINARY_PARAMETERS.fire_duration_value_bound.maximal,
                )
            )
        ]
        fire_chanel_boundary_infractions = [
            DurationChanelInfraction(
                event_index=event_index,
                value=fire_event.chanel,
                value_min=JSON_BINARY_PARAMETERS.fire_chanel_value_bound.minimal,
                value_max=JSON_BINARY_PARAMETERS.fire_chanel_value_bound.maximal,
            )
            for event_index, fire_event in enumerate(
                fire_events.specific_events,
            )
            if not (
                check_integer_bound(
                    fire_event.chanel,
                    JSON_BINARY_PARAMETERS.fire_chanel_value_bound.minimal,
                    JSON_BINARY_PARAMETERS.fire_chanel_value_bound.maximal,
                )
            )
        ]
        return fire_duration_boundary_infractions + fire_chanel_boundary_infractions
