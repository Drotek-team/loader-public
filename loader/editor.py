from typing import List, Optional, Tuple

from pydantic import NonNegativeInt

from loader.parameter.iostar_physic_parameter import IostarPhysicParameter
from loader.report.autopilot_format_report.autopilot_format_report import DronePx4Report

from .report.autopilot_format_report import DanceSizeInfraction
from .report.base import BaseReport
from .report.collision_report.migration.show_position_frames import (
    ShowPositionFrames,
)
from .report.collision_report.show_position_frames_collision_report import (
    CollisionInfraction,
    su_to_spf,
)
from .report.global_report import (
    GlobalReport,
)
from .report.performance_report.show_trajectory_performance_report import (
    PerformanceInfraction,
    su_to_stp,
)
from .show_env.iostar_json.iostar_json_gcs import IostarJsonGcs
from .show_env.migration_dp_binary.drone_encoding import (
    DanceSizeInformation,
    get_dance_size_information,
)
from .show_env.migration_sp_ijg.ijg_to_su import ijg_to_su
from .show_env.migration_sp_ijg.su_to_ijg import su_to_ijg
from .show_env.migration_sp_ijg.su_to_scg import ShowConfigurationGcs, su_to_scg
from .show_env.migration_sp_su.su_to_sp import su_to_sp
from .show_env.show_user import DroneUser, ShowUser


class ReportError(Exception):
    """Exception raised when a report is invalid."""

    def __init__(self, report: BaseReport) -> None:
        self.report = report
        message = f"Report is invalid, found {report.get_nb_errors()} errors"
        super().__init__(message)


def create_empty_show_user(nb_drones: NonNegativeInt) -> ShowUser:
    """Return an ShowUser object with 'nb_drones' user drones. These drones contains no events."""
    if nb_drones <= 0:
        msg = f"nb_drones must be positive, not {nb_drones}"
        raise ValueError(msg)
    return ShowUser(
        drones_user=[
            DroneUser(
                index=drone_index,
                position_events=[],
                color_events=[],
                fire_events=[],
            )
            for drone_index in range(nb_drones)
        ],
    )


def create_show_position_frames_from_frames_positions(
    frame_start: int,
    frame_end: int,
    drone_indices: List[int],
    frames_positions: List[List[Tuple[float, float, float]]],
) -> ShowPositionFrames:
    """Return a ShowPositionFrames from frames_positions."""
    return ShowPositionFrames.create_from_frames_positions(
        frame_start,
        frame_end,
        drone_indices,
        frames_positions,
    )


def create_show_position_frames_from_show_user(
    show_user: ShowUser,
) -> ShowPositionFrames:
    """Return a ShowPositionFrame from a ShowUser."""
    return su_to_spf(show_user)


def get_performance_infractions(
    show_user: ShowUser,
    *,
    physic_parameter: Optional[IostarPhysicParameter] = None,
) -> List[PerformanceInfraction]:
    """Return all the performance infractions from show_user ordered by drone and by slice."""
    return PerformanceInfraction.generate(su_to_stp(show_user), physic_parameter=physic_parameter)


def get_collision_infractions(
    show_position_frames: ShowPositionFrames,
    *,
    collision_distance: Optional[float] = None,
) -> List[CollisionInfraction]:
    """Return all the collision infractions from show_position_frames ordered by slice."""
    return CollisionInfraction.generate(show_position_frames, collision_distance=collision_distance)


def get_dance_size_infractions(show_user: ShowUser) -> List[DanceSizeInfraction]:
    """Return all dance size infractions from show_user ordered by drones."""
    autopilot_format = su_to_sp(show_user)
    return [
        dance_size_infraction
        for drone_px4 in autopilot_format
        if (drone_px4_report := DronePx4Report.generate(drone_px4)) is not None
        if (dance_size_infraction := drone_px4_report.dance_size_infraction) is not None
    ]


def get_dance_size_informations(show_user: ShowUser) -> List[DanceSizeInformation]:
    autopilot_format_drones = su_to_sp(show_user)
    return [
        get_dance_size_information(autopilot_format_drone)
        for autopilot_format_drone in autopilot_format_drones
    ]


def generate_report_from_show_user(
    show_user: ShowUser,
    *,
    without_takeoff_format: bool = False,
    physic_parameter: Optional[IostarPhysicParameter] = None,
) -> GlobalReport:
    """Return a global report from show_user."""
    return GlobalReport.generate(
        show_user,
        without_takeoff_format=without_takeoff_format,
        physic_parameter=physic_parameter,
    )


def generate_report_from_iostar_json_gcs_string(
    iostar_json_gcs_string: str,
    *,
    without_takeoff_format: bool = False,
    physic_parameter: Optional[IostarPhysicParameter] = None,
) -> GlobalReport:
    """Return a global report from iostar_json_gcs_string."""
    iostar_json_gcs = IostarJsonGcs.parse_raw(iostar_json_gcs_string)
    show_user = ijg_to_su(iostar_json_gcs)
    return GlobalReport.generate(
        show_user,
        without_takeoff_format=without_takeoff_format,
        physic_parameter=physic_parameter,
    )


def get_show_configuration_from_iostar_json_gcs_string(
    iostar_json_gcs_string: str,
) -> ShowConfigurationGcs:
    """Return ShowConfigurationGcs based on iostar_json_gcs_string."""
    iostar_json_gcs = IostarJsonGcs.parse_raw(iostar_json_gcs_string)
    show_user = ijg_to_su(iostar_json_gcs)
    return su_to_scg(show_user)


def convert_show_user_to_iostar_json_gcs(show_user: ShowUser) -> IostarJsonGcs:
    """Return iostar json gcs string based on show_user."""
    return su_to_ijg(show_user)


def convert_iostar_json_gcs_string_to_show_user(
    iostar_json_gcs_string: str,
) -> ShowUser:
    """Return show_user based on iostar json gcs string."""
    iostar_json_gcs = IostarJsonGcs.parse_raw(iostar_json_gcs_string)
    return ijg_to_su(iostar_json_gcs)


def get_verified_iostar_json_gcs(iostar_json_gcs_string: str) -> IostarJsonGcs:
    """Return iostar_json_gcs from iostar_json_gcs_string."""
    iostar_json_gcs = IostarJsonGcs.parse_raw(iostar_json_gcs_string)
    show_user = ijg_to_su(iostar_json_gcs)
    global_report = GlobalReport.generate(show_user)
    if global_report.get_nb_errors() > 0:
        raise ReportError(global_report)
    return su_to_ijg(show_user)
