# pyright: reportIncompatibleMethodOverride=false
from typing import List, Optional

from loader.reports.base import BaseReport
from loader.schemas.drone_px4 import DronePx4
from loader.schemas.drone_px4.events import ColorEvents, FireEvents, PositionEvents

from .events_format_infractions import (
    ColorBoundaryInfraction,
    FireChannelInfraction,
    FireDurationInfraction,
    PositionBoundaryInfraction,
    TimecodeReport,
)


class PositionEventsReport(BaseReport):
    timecode_report: Optional[TimecodeReport] = None
    position_infractions: List[PositionBoundaryInfraction] = []

    @classmethod
    def generate(
        cls,
        position_events: PositionEvents,
    ) -> "PositionEventsReport":
        timecode_report = TimecodeReport.generate_or_none(position_events)
        coordinate_infractions = PositionBoundaryInfraction.generate(
            position_events,
        )
        return PositionEventsReport(
            timecode_report=timecode_report,
            position_infractions=coordinate_infractions,
        )


class ColorEventsReport(BaseReport):
    timecode_report: Optional[TimecodeReport] = None
    color_infractions: List[ColorBoundaryInfraction] = []

    @classmethod
    def generate(
        cls,
        color_events: ColorEvents,
    ) -> "ColorEventsReport":
        timecode_report = TimecodeReport.generate_or_none(
            color_events,
        )
        chrome_infractions = ColorBoundaryInfraction.generate(
            color_events,
        )
        return ColorEventsReport(
            timecode_report=timecode_report,
            color_infractions=chrome_infractions,
        )


class FireEventsReport(BaseReport):
    timecode_report: Optional[TimecodeReport] = None
    duration_infractions: List[FireDurationInfraction] = []
    channel_infractions: List[FireChannelInfraction] = []

    @classmethod
    def generate(
        cls,
        fire_events: FireEvents,
    ) -> "FireEventsReport":
        timecode_report = TimecodeReport.generate_or_none(
            fire_events,
        )
        duration_infractions = FireDurationInfraction.generate(fire_events)
        channel_infractions = FireChannelInfraction.generate(fire_events)
        return FireEventsReport(
            timecode_report=timecode_report,
            duration_infractions=duration_infractions,
            channel_infractions=channel_infractions,
        )


class EventsFormatReport(BaseReport):
    drone_index: int
    position_events_report: Optional[PositionEventsReport] = None
    color_events_report: Optional[ColorEventsReport] = None
    fire_events_report: Optional[FireEventsReport] = None

    @classmethod
    def generate(
        cls,
        drone_px4: DronePx4,
    ) -> "EventsFormatReport":
        position_events_report = PositionEventsReport.generate_or_none(
            drone_px4.position_events,
        )
        color_events_report = ColorEventsReport.generate_or_none(
            drone_px4.color_events,
        )
        fire_events_report = FireEventsReport.generate_or_none(
            drone_px4.fire_events,
        )
        return EventsFormatReport(
            drone_index=drone_px4.index,
            position_events_report=position_events_report,
            color_events_report=color_events_report,
            fire_events_report=fire_events_report,
        )
