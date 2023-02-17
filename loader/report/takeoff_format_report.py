from typing import List, Optional, Tuple

import numpy as np

from loader.parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from loader.report.base import BaseInfraction, BaseReport
from loader.show_env.show_user import DroneUser, ShowUser


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
        if (
            np.abs(
                (second_time - first_time) - TAKEOFF_PARAMETER.takeoff_duration_second,
            )
            > TAKEOFF_PARAMETER.takeoff_total_duration_tolerance
        ):
            return TakeoffDurationInfraction(
                first_time=first_time,
                second_time=second_time,
                takeoff_duration=TAKEOFF_PARAMETER.takeoff_duration_second,
                tolerance=TAKEOFF_PARAMETER.takeoff_total_duration_tolerance,
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
            or first_position[2] + TAKEOFF_PARAMETER.takeoff_altitude_meter_min
            > second_position[2]
            or second_position[2]
            > first_position[2] + TAKEOFF_PARAMETER.takeoff_altitude_meter_max
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
    ) -> Optional["TakeoffReport"]:
        duration_infraction = TakeoffDurationInfraction.generate(
            drone_user,
        )
        position_infraction = TakeoffPositionInfraction.generate(
            drone_user,
        )
        if duration_infraction is not None or position_infraction is not None:
            return TakeoffReport(
                duration_infraction=duration_infraction,
                position_infraction=position_infraction,
            )
        return None


class MinimalPositionEventsNumber(BaseReport):
    events_number: int

    @classmethod
    def generate(
        cls,
        drone_user: DroneUser,
    ) -> Optional["MinimalPositionEventsNumber"]:
        if len(drone_user.position_events) >= 2:
            return None
        return MinimalPositionEventsNumber(
            events_number=len(drone_user.position_events),
        )


class DroneUserReport(BaseReport):
    minimal_position_event: Optional[MinimalPositionEventsNumber] = None
    takeoff: Optional[TakeoffReport] = None

    @classmethod
    def generate(
        cls,
        drone_user: DroneUser,
    ) -> Optional["DroneUserReport"]:
        minimal_position_event_report = MinimalPositionEventsNumber.generate(
            drone_user,
        )
        if minimal_position_event_report is not None:
            return DroneUserReport(
                minimal_position_event=minimal_position_event_report,
            )
        takeoff_report = TakeoffReport.generate(drone_user)
        if takeoff_report is not None:
            return DroneUserReport(takeoff=takeoff_report)
        return None


class TakeoffFormatReport(BaseReport):
    drone_users: List[DroneUserReport] = []

    @classmethod
    def generate(
        cls,
        show_user: ShowUser,
    ) -> Optional["TakeoffFormatReport"]:
        drone_user_reports = [
            drone_user_report
            for drone_user in show_user.drones_user
            if (drone_user_report := DroneUserReport.generate(drone_user)) is not None
        ]
        if not (drone_user_reports):
            return None
        return TakeoffFormatReport(drone_users=drone_user_reports)
