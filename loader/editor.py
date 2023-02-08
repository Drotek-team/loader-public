import json
from typing import Any, Dict

from pydantic import NonNegativeInt

from .check.all_check_from_show_user import (
    apply_all_check_from_show_user,
    apply_show_px4_check,
)
from .check.collision_check.migration.show_simulation import ShowSimulation
from .check.collision_check.show_simulation_collision_check import (
    apply_show_simulation_check_to_show_simulation,
)
from .check.performance_check.performance_evaluation import (
    METRICS_RANGE,
    METRICS_RANGE_COPY,
    Metric,
    MetricRange,
)
from .check.performance_check.show_trajectory_performance_check import (
    apply_show_trajectory_performance_check,
)
from .report.report import Contenor
from .show_env.iostar_json.iostar_json_gcs import IostarJsonGcs
from .show_env.migration_sp_ijg.ijg_to_su import ijg_to_su
from .show_env.migration_sp_ijg.su_to_ijg import su_to_ijg
from .show_env.migration_sp_ijg.su_to_scg import su_to_scg
from .show_env.show_user.show_user import DroneUser, ShowUser


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


def get_performance_infractions(
    show_user: ShowUser,
    update_metrics_range: Dict[Metric, MetricRange],
) -> Contenor:
    """Return a contenor with all the performance infractions ordered by drone and by slice."""
    METRICS_RANGE.update(update_metrics_range)
    show_trajectory_performance_check = apply_show_trajectory_performance_check(
        show_user,
    )
    METRICS_RANGE.update(METRICS_RANGE_COPY)
    return show_trajectory_performance_check


def get_collision_infractions(show_simulation: ShowSimulation) -> Contenor:
    """Return a contenor with all the collision ordered by slice."""
    return apply_show_simulation_check_to_show_simulation(show_simulation)


def get_dance_size_infractions(show_user: ShowUser) -> Contenor:
    """Return a contenor with the dance size report ordered by drones."""
    return apply_show_px4_check(show_user)


def get_drotek_check_from_show_user(show_user: ShowUser) -> str:
    """Return a report of show user validity as a string. The show user is valid if the report is empty."""
    show_check_report = apply_all_check_from_show_user(show_user)
    return show_check_report.display_message()


def get_drotek_check_from_iostar_json_gcs_string(iostar_json_gcs_string: str) -> str:
    """Return a report of iostar json gcs string validity as a string. The show user is valid if the report is empty."""
    iostar_json_gcs = IostarJsonGcs.parse_raw(iostar_json_gcs_string)
    show_user = ijg_to_su(iostar_json_gcs)
    show_check_report = apply_all_check_from_show_user(show_user)
    return show_check_report.display_message()


def get_drotek_json_check_from_iostar_json_gcs_string(
    iostar_json_gcs_string: str,
) -> Dict[str, Any]:
    """Return a report of iostar json gcs string validity in the dict format. The show user is valid if the report is empty."""
    iostar_json_gcs = IostarJsonGcs.parse_raw(iostar_json_gcs_string)
    show_user = ijg_to_su(iostar_json_gcs)
    show_check_report = apply_all_check_from_show_user(show_user)
    return show_check_report.get_json()


def get_show_configuration_from_iostar_json_gcs_string(
    iostar_json_gcs_string: str,
) -> Dict[str, Any]:
    """Return the show configuration in the dict format from an iostar json gcs string."""
    iostar_json_gcs = IostarJsonGcs.parse_raw(iostar_json_gcs_string)
    show_user = ijg_to_su(iostar_json_gcs)
    show_configuration_gcs = su_to_scg(show_user)
    return json.loads(show_configuration_gcs.json())


def export_show_user_to_iostar_json_gcs_string(
    show_user: ShowUser,
) -> str:
    """Return a check iostar json gcs from a show user object."""
    return su_to_ijg(show_user).json()


def import_iostar_json_gcs_string_to_show_user(iostar_json_gcs_string: str) -> ShowUser:
    """Return a check show user from an iostar json gcs string."""
    iostar_json_gcs = IostarJsonGcs.parse_raw(iostar_json_gcs_string)
    return ijg_to_su(iostar_json_gcs)


def get_verified_iostar_json_gcs(iostar_json_gcs_string: str) -> str:
    """Return a check iostar json gcs string from an iostar json gcs string."""
    iostar_json_gcs = IostarJsonGcs.parse_raw(iostar_json_gcs_string)
    show_user = ijg_to_su(iostar_json_gcs)
    show_check_report = apply_all_check_from_show_user(show_user)
    if not (show_check_report.user_validation):
        raise ValueError(show_check_report.display_message())
    return su_to_ijg(show_user).json()
