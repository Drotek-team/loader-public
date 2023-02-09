from abc import ABC
from typing import List, Optional, Tuple

import numpy as np

from loader.parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from loader.report.report import BaseReport
from loader.show_env.show_user.show_user import DroneUser, ShowUser


class TakeoffReport(BaseReport, ABC):
    pass


class OneEventTakeoffDurationInfraction(BaseReport):
    frame: int


def one_event_takeoff_duration_check(
    drone_user: DroneUser,
) -> Optional[OneEventTakeoffDurationInfraction]:
    if drone_user.position_events[0].frame != 0:
        return OneEventTakeoffDurationInfraction(
            frame=drone_user.position_events[0].frame,
        )
    return None


class OneEventTakeoffPositionInfraction(BaseReport):
    altitude: float


def one_event_takeoff_xyz_check(
    drone_user: DroneUser,
) -> Optional[OneEventTakeoffPositionInfraction]:
    first_position = drone_user.position_events[0].xyz
    if first_position[2] == 0.0:
        return OneEventTakeoffPositionInfraction(altitude=first_position[2])
    return None


class OneEventTakeoffReport(TakeoffReport, BaseReport):
    duration_infraction: Optional[OneEventTakeoffDurationInfraction] = None
    position_infraction: Optional[OneEventTakeoffPositionInfraction] = None


def apply_one_event_takeoff_check(
    drone_user: DroneUser,
) -> Optional[OneEventTakeoffReport]:
    duration_infraction = one_event_takeoff_duration_check(drone_user)
    position_infraction = one_event_takeoff_xyz_check(drone_user)
    if duration_infraction is not None or position_infraction is not None:
        return OneEventTakeoffReport(
            duration_infraction=duration_infraction,
            position_infraction=position_infraction,
        )
    return None


class MultipleEventTakeoffDurationInfraction(BaseReport):
    first_time: float
    second_time: float
    takeoff_duration: float
    tolerance: float


def apply_multiple_event_takeoff_duration_check(
    drone_user: DroneUser,
) -> Optional[MultipleEventTakeoffDurationInfraction]:
    first_time = drone_user.position_events[0].absolute_time
    second_time = drone_user.position_events[1].absolute_time
    if (
        np.abs((second_time - first_time) - TAKEOFF_PARAMETER.takeoff_duration_second)
        > TAKEOFF_PARAMETER.takeoff_total_duration_tolerance
    ):
        return MultipleEventTakeoffDurationInfraction(
            first_time=first_time,
            second_time=second_time,
            takeoff_duration=TAKEOFF_PARAMETER.takeoff_duration_second,
            tolerance=TAKEOFF_PARAMETER.takeoff_total_duration_tolerance,
        )
    return None


class MultipleEventTakeoffPositionInfraction(BaseReport):
    first_position: Tuple[float, float, float]
    second_position: Tuple[float, float, float]


def apply_multiple_event_takeoff_position_check(
    drone_user: DroneUser,
) -> Optional[MultipleEventTakeoffPositionInfraction]:
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
        return MultipleEventTakeoffPositionInfraction(
            first_position=first_position,
            second_position=second_position,
        )
    return None


class MultipleEventsTakeoffReport(TakeoffReport, BaseReport):
    duration_infraction: Optional[MultipleEventTakeoffDurationInfraction] = None
    position_infraction: Optional[MultipleEventTakeoffPositionInfraction] = None


def apply_multiple_events_takeoff_check(
    drone_user: DroneUser,
) -> Optional[MultipleEventsTakeoffReport]:
    duration_infraction = apply_multiple_event_takeoff_duration_check(drone_user)
    position_infraction = apply_multiple_event_takeoff_position_check(drone_user)
    if duration_infraction is not None or position_infraction is not None:
        return MultipleEventsTakeoffReport(
            duration_infraction=duration_infraction,
            position_infraction=position_infraction,
        )
    return None


def apply_takeoff_report(
    drone_user: DroneUser,
) -> Optional[TakeoffReport]:
    if not (drone_user.position_events):
        msg = "This check can not operate on a drone without position events"
        raise ValueError(msg)
    if len(drone_user.position_events) == 1:
        return apply_one_event_takeoff_check(drone_user)
    return apply_multiple_events_takeoff_check(drone_user)


class MinimalPositionEventsNumber(BaseReport):
    events_number: int


def apply_minimal_position_events_number_report(
    drone_user: DroneUser,
) -> Optional[MinimalPositionEventsNumber]:
    # Improve: finir la discussion convention 1 position event
    if len(drone_user.position_events) == 1 or len(drone_user.position_events) >= 3:
        return None
    return MinimalPositionEventsNumber(events_number=len(drone_user.position_events))


class DroneUserReport(BaseReport):
    minimal_position_event_report: Optional[MinimalPositionEventsNumber] = None
    takeoff_report: Optional[TakeoffReport] = None


def get_drone_user_report(
    drone_user: DroneUser,
) -> Optional[DroneUserReport]:
    minimal_position_event_report = apply_minimal_position_events_number_report(
        drone_user,
    )
    if minimal_position_event_report is not None:
        return DroneUserReport(
            minimal_position_event_report=minimal_position_event_report,
        )
    takeoff_report = apply_takeoff_report(drone_user)
    if takeoff_report is not None:
        return DroneUserReport(takeoff_report=takeoff_report)
    return None


class ShowUserReport(BaseReport):
    drone_user_reports: List[DroneUserReport]


def get_show_user_report(
    show_user: ShowUser,
) -> Optional[ShowUserReport]:
    drone_user_reports = [
        drone_user_report
        for drone_user in show_user.drones_user
        if (drone_user_report := get_drone_user_report(drone_user)) is not None
    ]
    if not (drone_user_reports):
        return None
    return ShowUserReport(drone_user_reports=drone_user_reports)
