from typing import List, Optional

from loader.reports.base import BaseReport
from loader.schemas.drone_px4 import DronePx4
from loader.schemas.drone_px4.events import (
    ColorEvents,
    FireEvents,
    PositionEvents,
)

from .events_format_infractions import (
    ChromeInfraction,
    CoordinateInfraction,
    DurationChanelInfraction,
    TimecodeReport,
)


class PositionEventsReport(BaseReport):
    timecode_report: Optional[TimecodeReport] = None
    coordinate_infractions: List[CoordinateInfraction] = []

    @classmethod
    def generate(
        cls,
        position_events: PositionEvents,
    ) -> "PositionEventsReport":
        timecode_report = TimecodeReport.generate_or_none(position_events)
        coordinate_infractions = CoordinateInfraction.generate(
            position_events,
        )
        return PositionEventsReport(
            timecode_report=timecode_report,
            coordinate_infractions=coordinate_infractions,
        )


class ColorEventsReport(BaseReport):
    timecode_report: Optional[TimecodeReport] = None
    chrome_infractions: List[ChromeInfraction] = []

    @classmethod
    def generate(
        cls,
        color_events: ColorEvents,
    ) -> "ColorEventsReport":
        timecode_report = TimecodeReport.generate_or_none(
            color_events,
        )
        chrome_infractions = ChromeInfraction.generate(
            color_events,
        )
        return ColorEventsReport(
            timecode_report=timecode_report,
            chrome_infractions=chrome_infractions,
        )


class FireEventsReport(BaseReport):
    timecode_report: Optional[TimecodeReport] = None
    duration_chanel_infractions: List[DurationChanelInfraction] = []

    @classmethod
    def generate(
        cls,
        fire_events: FireEvents,
    ) -> "FireEventsReport":
        timecode_report = TimecodeReport.generate_or_none(
            fire_events,
        )
        duration_chanel_infractions = DurationChanelInfraction.generate(fire_events)
        return FireEventsReport(
            timecode_report=timecode_report,
            duration_chanel_infractions=duration_chanel_infractions,
        )


class EventsFormatReport(BaseReport):
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
            position_events_report=position_events_report,
            color_events_report=color_events_report,
            fire_events_report=fire_events_report,
        )
