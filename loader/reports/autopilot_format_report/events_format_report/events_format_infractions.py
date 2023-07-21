# pyright: reportIncompatibleMethodOverride=false
from enum import Enum
from typing import List, Type, TypeVar

from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS, Bound
from loader.reports.base import BaseInfraction, BaseReport
from loader.schemas.drone_px4.events import ColorEvents, Events, FireEvents, PositionEvents

TIntegerBoundaryInfraction = TypeVar(
    "TIntegerBoundaryInfraction",
    bound="IntegerBoundaryInfraction",
)


class BoundaryKind(Enum):
    TIMECODE = "timecode"
    NORTH = "north"
    EAST = "east"
    DOWN = "down"
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    WHITE = "white"
    CHANNEL = "channel"
    DURATION = "duration"

    def get_bound(self) -> Bound:
        if self == self.TIMECODE:
            return JSON_BINARY_PARAMETERS.timecode_value_bound
        if self in [self.NORTH, self.EAST, self.DOWN]:
            return JSON_BINARY_PARAMETERS.coordinate_value_bound
        if self in [self.RED, self.GREEN, self.BLUE, self.WHITE]:
            return JSON_BINARY_PARAMETERS.chrome_value_bound
        if self == self.CHANNEL:
            return JSON_BINARY_PARAMETERS.fire_channel_value_bound
        if self == self.DURATION:
            return JSON_BINARY_PARAMETERS.fire_duration_value_bound
        raise NotImplementedError


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


class IntegerBoundaryInfraction(BaseInfraction):
    kind: str
    event_index: int
    value: int

    @classmethod
    def generate(
        cls: Type[TIntegerBoundaryInfraction],
        kinds: List[BoundaryKind],
        indices: List[int],
        events: Events,
    ) -> List["TIntegerBoundaryInfraction"]:
        bound = kinds[0].get_bound()
        return [
            cls(event_index=event_index, value=value, kind=kind.value)
            for event_index, event in enumerate(events)
            for index, kind in zip(indices, kinds)
            if not (
                check_integer_bound((value := event.get_data[index]), bound.minimal, bound.maximal)
            )
        ]


class TimecodeBoundaryInfraction(IntegerBoundaryInfraction):
    @classmethod
    def generate(
        cls: Type[TIntegerBoundaryInfraction],
        events: Events,
    ) -> List["TIntegerBoundaryInfraction"]:
        return super().generate([BoundaryKind.TIMECODE], [0], events)


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
    @classmethod
    def generate(
        cls: Type[TIntegerBoundaryInfraction],
        events: PositionEvents,
    ) -> List["TIntegerBoundaryInfraction"]:
        return super().generate(
            [BoundaryKind.NORTH, BoundaryKind.EAST, BoundaryKind.DOWN],
            [1, 2, 3],
            events,
        )


class ColorBoundaryInfraction(IntegerBoundaryInfraction):
    @classmethod
    def generate(
        cls: Type[TIntegerBoundaryInfraction],
        events: ColorEvents,
    ) -> List["TIntegerBoundaryInfraction"]:
        return super().generate(
            [BoundaryKind.RED, BoundaryKind.GREEN, BoundaryKind.BLUE, BoundaryKind.WHITE],
            [1, 2, 3, 4],
            events,
        )


class FireDurationInfraction(IntegerBoundaryInfraction):
    @classmethod
    def generate(
        cls: Type[TIntegerBoundaryInfraction],
        events: FireEvents,
    ) -> List["TIntegerBoundaryInfraction"]:
        return super().generate([BoundaryKind.DURATION], [2], events)


class FireChannelInfraction(IntegerBoundaryInfraction):
    @classmethod
    def generate(
        cls: Type[TIntegerBoundaryInfraction],
        events: FireEvents,
    ) -> List["TIntegerBoundaryInfraction"]:
        return super().generate([BoundaryKind.CHANNEL], [1], events)
