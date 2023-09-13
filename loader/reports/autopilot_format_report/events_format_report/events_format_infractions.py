# pyright: reportIncompatibleMethodOverride=false
from collections import defaultdict
from enum import Enum
from typing import Any, DefaultDict, List, Optional

from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS, Bound
from loader.reports.base import BaseInfraction, BaseInfractionsSummary, apply_func_on_optional_pair
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
        events: Events[Any],
    ) -> List["IncreasingFrameInfraction"]:
        frames = [event.frame for event in events]
        return [
            IncreasingFrameInfraction(
                event_index=event_index,
                previous_frame=frames[event_index - 1],
                frame=frames[event_index],
            )
            for event_index in range(1, len(frames))
            if frames[event_index - 1] >= frames[event_index]
        ]

    def summarize(self) -> "IncreasingFrameInfractionsSummary":
        return IncreasingFrameInfractionsSummary(
            nb_infractions=len(self),
            first=self,
            last=self,
        )


class IncreasingFrameInfractionsSummary(BaseInfractionsSummary):
    first: Optional[IncreasingFrameInfraction] = None
    last: Optional[IncreasingFrameInfraction] = None

    def __add__(
        self,
        other: "IncreasingFrameInfractionsSummary",
    ) -> "IncreasingFrameInfractionsSummary":
        first = apply_func_on_optional_pair(
            self.first,
            other.first,
            lambda x, y: x if x.frame < y.frame else y,
        )
        last = apply_func_on_optional_pair(
            self.last,
            other.last,
            lambda x, y: x if x.frame > y.frame else y,
        )

        return IncreasingFrameInfractionsSummary(
            nb_infractions=self.nb_infractions + other.nb_infractions,
            first=first,
            last=last,
        )


def check_integer_bound(integer: int, lower_bound: int, upper_bound: int) -> bool:
    return lower_bound <= integer and integer <= upper_bound


class BoundaryInfraction(BaseInfraction):
    event_index: int
    value: int

    @classmethod
    def generate(
        cls,
        events: Events[Any],
    ) -> DefaultDict[str, List["BoundaryInfraction"]]:
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

    def summarize(self) -> "BoundaryInfractionsSummary":
        return BoundaryInfractionsSummary(
            nb_infractions=len(self),
            min_boundary_infraction=self,
            max_boundary_infraction=self,
            first_boundary_infraction=self,
            last_boundary_infraction=self,
        )


class BoundaryInfractionsSummary(BaseInfractionsSummary):
    min_boundary_infraction: Optional[BoundaryInfraction] = None
    max_boundary_infraction: Optional[BoundaryInfraction] = None
    first_boundary_infraction: Optional[BoundaryInfraction] = None
    last_boundary_infraction: Optional[BoundaryInfraction] = None

    def __add__(self, other: "BoundaryInfractionsSummary") -> "BoundaryInfractionsSummary":
        min_value = apply_func_on_optional_pair(
            self.min_boundary_infraction,
            other.min_boundary_infraction,
            lambda x, y: x if x.value < y.value else y,
        )
        max_value = apply_func_on_optional_pair(
            self.max_boundary_infraction,
            other.max_boundary_infraction,
            lambda x, y: x if x.value > y.value else y,
        )
        first = apply_func_on_optional_pair(
            self.first_boundary_infraction,
            other.first_boundary_infraction,
            lambda x, y: x if x.event_index < y.event_index else y,
        )
        last = apply_func_on_optional_pair(
            self.last_boundary_infraction,
            other.last_boundary_infraction,
            lambda x, y: x if x.event_index > y.event_index else y,
        )

        return BoundaryInfractionsSummary(
            nb_infractions=self.nb_infractions + other.nb_infractions,
            min_boundary_infraction=min_value,
            max_boundary_infraction=max_value,
            first_boundary_infraction=first,
            last_boundary_infraction=last,
        )
