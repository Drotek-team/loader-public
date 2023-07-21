# pyright: reportIncompatibleMethodOverride=false
from typing import List

from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS
from loader.reports.base import BaseInfraction, BaseReport
from loader.schemas.drone_px4.events import ColorEvents, Events, FireEvents, PositionEvents


class IntegerBoundaryInfraction(BaseInfraction):
    event_index: int
    value: int


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


class TimecodeBoundaryInfraction(IntegerBoundaryInfraction):
    @classmethod
    def generate(
        cls,
        events: Events,
    ) -> List["TimecodeBoundaryInfraction"]:
        return [
            TimecodeBoundaryInfraction(
                event_index=event_index,
                value=frame,
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
    boundary_infractions: List[TimecodeBoundaryInfraction] = []
    increasing_infractions: List[IncreasingFrameInfraction] = []

    @classmethod
    def generate(
        cls,
        events: Events,
    ) -> "TimecodeReport":
        bound_infractions = TimecodeBoundaryInfraction.generate(events)
        increasing_infractions = IncreasingFrameInfraction.generate(events)
        return TimecodeReport(
            boundary_infractions=bound_infractions,
            increasing_infractions=increasing_infractions,
        )


class PositionBoundaryInfraction(IntegerBoundaryInfraction):
    axis: str

    @classmethod
    def generate(
        cls,
        position_events: PositionEvents,
    ) -> List["PositionBoundaryInfraction"]:
        return [
            PositionBoundaryInfraction(
                event_index=event_index,
                axis=axis,
                value=position_event.xyz[coordinate_index],
            )
            for event_index, position_event in enumerate(
                position_events.specific_events,
            )
            for coordinate_index, axis in enumerate(["north", "east", "down"])
            if not (
                check_integer_bound(
                    position_event.xyz[coordinate_index],
                    JSON_BINARY_PARAMETERS.coordinate_value_bound.minimal,
                    JSON_BINARY_PARAMETERS.coordinate_value_bound.maximal,
                )
            )
        ]


class ColorBoundaryInfraction(IntegerBoundaryInfraction):
    channel: str

    @classmethod
    def generate(
        cls,
        color_events: ColorEvents,
    ) -> List["ColorBoundaryInfraction"]:
        return [
            ColorBoundaryInfraction(
                event_index=event_index,
                channel=channel,
                value=color_event.rgbw[chrome_index],
            )
            for event_index, color_event in enumerate(
                color_events.specific_events,
            )
            for chrome_index, channel in enumerate(["red", "green", "blue", "white"])
            if not (
                check_integer_bound(
                    color_event.rgbw[chrome_index],
                    JSON_BINARY_PARAMETERS.chrome_value_bound.minimal,
                    JSON_BINARY_PARAMETERS.chrome_value_bound.maximal,
                )
            )
        ]


class FireDurationInfraction(IntegerBoundaryInfraction):
    @classmethod
    def generate(
        cls,
        fire_events: FireEvents,
    ) -> List["FireDurationInfraction"]:
        return [
            FireDurationInfraction(
                event_index=event_index,
                value=fire_event.duration,
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


class FireChannelInfraction(IntegerBoundaryInfraction):
    @classmethod
    def generate(
        cls,
        fire_events: FireEvents,
    ) -> List["FireChannelInfraction"]:
        return [
            FireChannelInfraction(
                event_index=event_index,
                value=fire_event.channel,
            )
            for event_index, fire_event in enumerate(
                fire_events.specific_events,
            )
            if not (
                check_integer_bound(
                    fire_event.channel,
                    JSON_BINARY_PARAMETERS.fire_channel_value_bound.minimal,
                    JSON_BINARY_PARAMETERS.fire_channel_value_bound.maximal,
                )
            )
        ]
