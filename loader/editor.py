from typing import Dict, List, Tuple

from pydantic import NonNegativeInt

from .check.all_check_from_show_user import (
    GlobalReport,
    GlobalReportSummary,
    get_global_report,
)
from .check.collision_check.migration.show_position_frames import (
    ShowPositionFrames,
)
from .check.collision_check.show_position_frames_collision_check import (
    CollisionInfraction,
    get_collision_infractions_from_show_position_frames,
    su_to_spf,
)
from .check.performance_check.performance_evaluation import (
    METRICS_RANGE,
    METRICS_RANGE_COPY,
    Metric,
    MetricRange,
)
from .check.performance_check.show_trajectory_performance_check import (
    PerformanceInfraction,
    get_performance_infractions_from_show_trajectory,
    su_to_stp,
)
from .check.show_px4_check import (
    DanceSizeInfraction,
    get_drone_px4_report,
)
from .report import BaseReport
from .show_env.iostar_json.iostar_json_gcs import IostarJsonGcs
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


def create_empty_show_user(drone_number: NonNegativeInt) -> ShowUser:
    """Return an ShowUser object with 'drone_number' user drones. These drones contains no events."""
    if drone_number <= 0:
        msg = f"drone_number must be positive, not {drone_number}"
        raise ValueError(msg)
    return ShowUser(
        drones_user=[
            DroneUser(
                index=drone_index,
                position_events=[],
                color_events=[],
                fire_events=[],
            )
            for drone_index in range(drone_number)
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
    update_metrics_range: Dict[Metric, MetricRange],
) -> List[PerformanceInfraction]:
    """Return all the performance infractions ordered by drone and by slice."""
    METRICS_RANGE.update(update_metrics_range)
    performance_infractions = get_performance_infractions_from_show_trajectory(
        su_to_stp(show_user),
    )
    METRICS_RANGE.update(METRICS_RANGE_COPY)
    return performance_infractions


def get_collision_infractions(
    show_position_frames: ShowPositionFrames,
) -> List[CollisionInfraction]:
    """Return all the collision infractions ordered by slice."""
    return get_collision_infractions_from_show_position_frames(show_position_frames)


def get_dance_size_infractions(show_user: ShowUser) -> List[DanceSizeInfraction]:
    """Return all dance size infractions ordered by drones."""
    show_px4 = su_to_sp(show_user)
    return [
        dance_size_infraction
        for drone_px4 in show_px4
        if (drone_px4_report := get_drone_px4_report(drone_px4)) is not None
        if (dance_size_infraction := drone_px4_report.dance_size_infraction) is not None
    ]


def generate_report_from_show_user(show_user: ShowUser) -> GlobalReport:
    """Return a report of show user validity."""
    return get_global_report(show_user)


def generate_report_summary_from_show_user(show_user: ShowUser) -> GlobalReportSummary:
    """Return a report of show user validity as a string. The show user is valid if the report is empty."""
    return generate_report_from_show_user(show_user).summary()


def generate_report_from_iostar_json_gcs_string(
    iostar_json_gcs_string: str,
) -> GlobalReport:
    """Return a report of iostar json gcs string validity as a string. The show user is valid if the report is empty."""
    iostar_json_gcs = IostarJsonGcs.parse_raw(iostar_json_gcs_string)
    show_user = ijg_to_su(iostar_json_gcs)
    return get_global_report(show_user)


def generate_report_summary_from_iostar_json_gcs_string(
    iostar_json_gcs_string: str,
) -> GlobalReportSummary:
    """Return a report of iostar json gcs string validity as a string. The show user is valid if the report is empty."""
    return generate_report_from_iostar_json_gcs_string(
        iostar_json_gcs_string,
    ).summary()


def get_show_configuration_from_iostar_json_gcs_string(
    iostar_json_gcs_string: str,
) -> ShowConfigurationGcs:
    """Return the show configuration in the dict format from an iostar json gcs string."""
    iostar_json_gcs = IostarJsonGcs.parse_raw(iostar_json_gcs_string)
    show_user = ijg_to_su(iostar_json_gcs)
    return su_to_scg(show_user)


def convert_show_user_to_iostar_json_gcs(show_user: ShowUser) -> IostarJsonGcs:
    """Return a check iostar json gcs from a show user object."""
    return su_to_ijg(show_user)


def convert_iostar_json_gcs_string_to_show_user(
    iostar_json_gcs_string: str,
) -> ShowUser:
    """Return a check show user from an iostar json gcs string."""
    iostar_json_gcs = IostarJsonGcs.parse_raw(iostar_json_gcs_string)
    return ijg_to_su(iostar_json_gcs)


def get_verified_iostar_json_gcs(iostar_json_gcs_string: str) -> IostarJsonGcs:
    """Return a check iostar json gcs string from an iostar json gcs string."""
    iostar_json_gcs = IostarJsonGcs.parse_raw(iostar_json_gcs_string)
    show_user = ijg_to_su(iostar_json_gcs)
    show_check_report = get_global_report(show_user)
    if show_check_report.get_nb_errors() > 0:
        raise ReportError(show_check_report)
    return su_to_ijg(show_user)
