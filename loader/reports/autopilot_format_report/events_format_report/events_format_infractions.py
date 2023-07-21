# pyright: reportIncompatibleMethodOverride=false
from collections import defaultdict
from enum import Enum
from typing import DefaultDict, Dict, List

from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS, Bound
from loader.reports.base import BaseInfraction
from loader.schemas.drone_px4.events import ColorEvents, Events, FireEvents, PositionEvents


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


class BoundaryInfraction(BaseInfraction):
    event_index: int
    value: int

    @classmethod
    def generate(
        cls,
        events: Events,
    ) -> Dict[str, List["BoundaryInfraction"]]:
        if isinstance(events, PositionEvents):
            boundary_kinds = [
                BoundaryKind.TIMECODE,
                BoundaryKind.NORTH,
                BoundaryKind.EAST,
                BoundaryKind.DOWN,
            ]
        elif isinstance(events, ColorEvents):
            boundary_kinds = [
                BoundaryKind.TIMECODE,
                BoundaryKind.RED,
                BoundaryKind.GREEN,
                BoundaryKind.BLUE,
                BoundaryKind.WHITE,
            ]
        elif isinstance(events, FireEvents):
            boundary_kinds = [BoundaryKind.TIMECODE, BoundaryKind.CHANNEL, BoundaryKind.DURATION]
        else:
            raise NotImplementedError

        bounds = [kind.get_bound() for kind in boundary_kinds]
        infractions: DefaultDict[str, List[BoundaryInfraction]] = defaultdict(list)
        for event_index, event in enumerate(events):
            for kind, bound, value in zip(boundary_kinds, bounds, event.get_data):
                if not (
                    check_integer_bound(
                        value,
                        bound.minimal,
                        bound.maximal,
                    )
                ):
                    infractions[kind.value].append(cls(event_index=event_index, value=value))
        return infractions
