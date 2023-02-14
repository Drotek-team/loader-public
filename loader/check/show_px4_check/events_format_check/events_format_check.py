from typing import List, Optional

from loader.report import BaseReport
from loader.show_env.show_px4.drone_px4.drone_px4 import DronePx4
from loader.show_env.show_px4.drone_px4.events.color_events import ColorEvents
from loader.show_env.show_px4.drone_px4.events.fire_events import FireEvents
from loader.show_env.show_px4.drone_px4.events.position_events import PositionEvents

from .events_format_check_tools import (
    IntegerBoundaryInfraction,
    TimecodeReport,
    get_chrome_infractions,
    get_coordinate_infractions,
    get_duration_chanel_infractions,
    get_timecode_report,
)


class PositionEventsReport(BaseReport):
    timecode_report: Optional[TimecodeReport] = None
    coordinate_infractions: List[IntegerBoundaryInfraction] = []


def get_position_events_report(
    position_events: PositionEvents,
) -> Optional[PositionEventsReport]:
    timecode_report = get_timecode_report(position_events)
    coordinate_infractions = get_coordinate_infractions(
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
    chrome_infractions: List[IntegerBoundaryInfraction] = []


def get_color_events_report(
    color_events: ColorEvents,
) -> Optional[ColorEventsReport]:
    timecode_report = get_timecode_report(
        color_events,
    )
    chrome_infractions = get_chrome_infractions(
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
    duration_chanel_infractions: List[IntegerBoundaryInfraction] = []


def get_fire_events_report(
    fire_events: FireEvents,
) -> Optional[FireEventsReport]:
    timecode_report = get_timecode_report(
        fire_events,
    )
    duration_chanel_infractions = get_duration_chanel_infractions(fire_events)
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


def get_events_format_report(
    drone_px4: DronePx4,
) -> Optional[EventsFormatReport]:
    position_events_report = get_position_events_report(
        drone_px4.position_events,
    )
    color_events_report = get_color_events_report(
        drone_px4.color_events,
    )
    fire_events_report = get_fire_events_report(
        drone_px4.fire_events,
    )
    if position_events_report or color_events_report or fire_events_report:
        return EventsFormatReport(
            position_events_report=position_events_report,
            color_events_report=color_events_report,
            fire_events_report=fire_events_report,
        )
    return None
