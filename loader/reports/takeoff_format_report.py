from typing import List, Optional, Tuple

import numpy as np

from loader.parameters import TAKEOFF_PARAMETERS
from loader.reports.base import BaseInfraction, BaseReport
from loader.schemas.show_user import DroneUser, ShowUser


class TakeoffDurationInfraction(BaseInfraction):
    first_time: float
    second_time: float
    takeoff_duration: float
    tolerance: float

    @classmethod
    def generate(
        cls,
        drone_user: DroneUser,
    ) -> Optional["TakeoffDurationInfraction"]:
        first_time = drone_user.position_events[0].absolute_time
        second_time = drone_user.position_events[1].absolute_time
        if not np.allclose(
            second_time - first_time,
            TAKEOFF_PARAMETERS.takeoff_duration_second,
            atol=TAKEOFF_PARAMETERS.takeoff_total_duration_tolerance,
        ):
            return TakeoffDurationInfraction(
                first_time=first_time,
                second_time=second_time,
                takeoff_duration=TAKEOFF_PARAMETERS.takeoff_duration_second,
                tolerance=TAKEOFF_PARAMETERS.takeoff_total_duration_tolerance,
            )
        return None


class TakeoffPositionInfraction(BaseInfraction):
    first_position: Tuple[float, float, float]
    second_position: Tuple[float, float, float]

    @classmethod
    def generate(
        cls,
        drone_user: DroneUser,
    ) -> Optional["TakeoffPositionInfraction"]:
        first_position = drone_user.position_events[0].xyz
        second_position = drone_user.position_events[1].xyz
        if (
            first_position[0] != second_position[0]
            or first_position[1] != second_position[1]
            or first_position[2] + TAKEOFF_PARAMETERS.takeoff_altitude_meter_min
            > second_position[2]
            or second_position[2]
            > first_position[2] + TAKEOFF_PARAMETERS.takeoff_altitude_meter_max
        ):
            return TakeoffPositionInfraction(
                first_position=first_position,
                second_position=second_position,
            )
        return None


class TakeoffReport(BaseReport):
    duration_infraction: Optional[TakeoffDurationInfraction] = None
    position_infraction: Optional[TakeoffPositionInfraction] = None

    @classmethod
    def generate(
        cls,
        drone_user: DroneUser,
    ) -> "TakeoffReport":
        duration_infraction = TakeoffDurationInfraction.generate(
            drone_user,
        )
        position_infraction = TakeoffPositionInfraction.generate(
            drone_user,
        )
        return TakeoffReport(
            duration_infraction=duration_infraction,
            position_infraction=position_infraction,
        )


class MinimumPositionEventsInfraction(BaseInfraction):
    events_number: int

    @classmethod
    def generate(
        cls,
        drone_user: DroneUser,
    ) -> Optional["MinimumPositionEventsInfraction"]:
        if len(drone_user.position_events) >= 2:
            return None
        return MinimumPositionEventsInfraction(
            events_number=len(drone_user.position_events),
        )


class DroneUserReport(BaseReport):
    minimal_position_event: Optional[MinimumPositionEventsInfraction] = None
    takeoff: Optional[TakeoffReport] = None

    @classmethod
    def generate(
        cls,
        drone_user: DroneUser,
    ) -> "DroneUserReport":
        minimal_position_event_report = MinimumPositionEventsInfraction.generate(
            drone_user,
        )
        if minimal_position_event_report is not None:
            return DroneUserReport(
                minimal_position_event=minimal_position_event_report,
            )
        takeoff_report = TakeoffReport.generate_or_none(drone_user)
        return DroneUserReport(takeoff=takeoff_report)


class TakeoffFormatReport(BaseReport):
    drone_users: List[DroneUserReport] = []

    @classmethod
    def generate(
        cls,
        show_user: ShowUser,
    ) -> "TakeoffFormatReport":
        drone_user_reports = [
            drone_user_report
            for drone_user in show_user.drones_user
            if (drone_user_report := DroneUserReport.generate_or_none(drone_user)) is not None
        ]
        return TakeoffFormatReport(drone_users=drone_user_reports)
