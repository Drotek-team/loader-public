# pyright: reportIncompatibleMethodOverride=false
from typing import Dict, List, Optional

from loader.reports.base import BaseReport
from loader.schemas.drone_px4 import DronePx4
from loader.schemas.drone_px4.events import Events

from .events_format_infractions import BoundaryInfraction, IncreasingFrameInfraction


class EventsReport(BaseReport):
    increasing_infractions: List[IncreasingFrameInfraction]
    boundary_infractions: Dict[str, List[BoundaryInfraction]]

    @classmethod
    def generate(
        cls,
        events: Events,
    ) -> "EventsReport":
        increasing_infractions = IncreasingFrameInfraction.generate(events)
        boundary_infractions = BoundaryInfraction.generate(events)
        return EventsReport(
            increasing_infractions=increasing_infractions,
            boundary_infractions=boundary_infractions,
        )


class EventsFormatReport(BaseReport):
    drone_index: int
    position_events_report: Optional[EventsReport]
    color_events_report: Optional[EventsReport]
    fire_events_report: Optional[EventsReport]

    @classmethod
    def generate(
        cls,
        drone_px4: DronePx4,
    ) -> "EventsFormatReport":
        position_events_report = EventsReport.generate_or_none(drone_px4.position_events)
        color_events_report = EventsReport.generate_or_none(drone_px4.color_events)
        fire_events_report = EventsReport.generate_or_none(drone_px4.fire_events)
        return EventsFormatReport(
            drone_index=drone_px4.index,
            position_events_report=position_events_report,
            color_events_report=color_events_report,
            fire_events_report=fire_events_report,
        )
