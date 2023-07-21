# pyright: reportIncompatibleMethodOverride=false
from typing import List, Optional, Tuple

import numpy as np
from tqdm import tqdm

from loader.parameters import TAKEOFF_PARAMETERS
from loader.reports.base import BaseInfraction, BaseReport
from loader.schemas.show_user import DroneUser, ShowUser


class TakeoffDurationInfraction(BaseInfraction):
    start_frame: float  # frame
    end_frame: float  # frame
    duration: float  # second

    @classmethod
    def generate(
        cls,
        drone_user: DroneUser,
    ) -> Optional["TakeoffDurationInfraction"]:
        first_event = drone_user.position_events[0]
        second_event = drone_user.position_events[1]
        duration = second_event.absolute_time - first_event.absolute_time
        if not np.allclose(
            duration,
            TAKEOFF_PARAMETERS.takeoff_duration_second,
            atol=TAKEOFF_PARAMETERS.takeoff_total_duration_tolerance,
        ):
            return TakeoffDurationInfraction(
                start_frame=first_event.frame,
                end_frame=second_event.frame,
                duration=duration,
            )
        return None


class TakeoffPositionInfraction(BaseInfraction):
    start_position: Tuple[float, float, float]
    end_position: Tuple[float, float, float]

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
                start_position=first_position,
                end_position=second_position,
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
    drone_index: int
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
                drone_index=drone_user.index,
                minimal_position_event=minimal_position_event_report,
            )
        takeoff_report = TakeoffReport.generate_or_none(drone_user)
        return DroneUserReport(drone_index=drone_user.index, takeoff=takeoff_report)


class TakeoffFormatReport(BaseReport):
    drone_users: List[DroneUserReport] = []

    @classmethod
    def generate(
        cls,
        show_user: ShowUser,
    ) -> "TakeoffFormatReport":
        drone_user_reports = [
            drone_user_report
            for drone_user in tqdm(show_user.drones_user, desc="Checking takeoffs", unit="drone")
            if len(drone_user_report := DroneUserReport.generate(drone_user))
        ]
        return TakeoffFormatReport(drone_users=drone_user_reports)
