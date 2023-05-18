from typing import List, Optional

from loader.report.base import BaseReport
from loader.show_env.drone_px4 import DronePx4
from loader.show_env.drone_px4.events import (
    ColorEvents,
    FireEvents,
    PositionEvents,
)

from .events_format_report_tools import (
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
    ) -> Optional["PositionEventsReport"]:
        timecode_report = TimecodeReport.generate(position_events)
        coordinate_infractions = CoordinateInfraction.generate(
            position_events,
        )
        if timecode_report or coordinate_infractions:
            return PositionEventsReport(
                timecode_report=timecode_report,
                coordinate_infractions=coordinate_infractions,
            )
        return None


class ColorEventsReport(BaseReport):
    timecode_report: Optional[TimecodeReport] = None
    chrome_infractions: List[ChromeInfraction] = []

    @classmethod
    def generate(
        cls,
        color_events: ColorEvents,
    ) -> Optional["ColorEventsReport"]:
        timecode_report = TimecodeReport.generate(
            color_events,
        )
        chrome_infractions = ChromeInfraction.generate(
            color_events,
        )
        if timecode_report or chrome_infractions:
            return ColorEventsReport(
                timecode_report=timecode_report,
                chrome_infractions=chrome_infractions,
            )
        return None


class FireEventsReport(BaseReport):
    timecode_report: Optional[TimecodeReport] = None
    duration_chanel_infractions: List[DurationChanelInfraction] = []

    @classmethod
    def generate(
        cls,
        fire_events: FireEvents,
    ) -> Optional["FireEventsReport"]:
        timecode_report = TimecodeReport.generate(
            fire_events,
        )
        duration_chanel_infractions = DurationChanelInfraction.generate(fire_events)
        if timecode_report or duration_chanel_infractions:
            return FireEventsReport(
                timecode_report=timecode_report,
                duration_chanel_infractions=duration_chanel_infractions,
            )
        return None


class EventsFormatReport(BaseReport):
    position_events_report: Optional[PositionEventsReport] = None
    color_events_report: Optional[ColorEventsReport] = None
    fire_events_report: Optional[FireEventsReport] = None

    @classmethod
    def generate(
        cls,
        drone_px4: DronePx4,
    ) -> Optional["EventsFormatReport"]:
        position_events_report = PositionEventsReport.generate(
            drone_px4.position_events,
        )
        color_events_report = ColorEventsReport.generate(
            drone_px4.color_events,
        )
        fire_events_report = FireEventsReport.generate(
            drone_px4.fire_events,
        )
        if position_events_report or color_events_report or fire_events_report:
            return EventsFormatReport(
                position_events_report=position_events_report,
                color_events_report=color_events_report,
                fire_events_report=fire_events_report,
            )
        return None
