from typing import Tuple

from .check.all_check_from_show_user_procedure import (
    apply_all_check_from_show_user_procedure,
)
from .check.show_check_report import ShowCheckReport
from .show_env.iostar_json.iostar_json import IostarJson
from .show_env.iostar_json.iostar_json_gcs import IostarJsonGcs
from .show_env.migration_sp_ij.ij_to_sp_procedure import ij_to_sp_procedure
from .show_env.migration_sp_ij.sp_to_ij_procedure import sp_to_ij_procedure
from .show_env.migration_sp_ijg.ijg_to_sp_procedure import ijg_to_sp_procedure
from .show_env.migration_sp_ijg.sp_to_ijg_procedure import sp_to_ijg_procedure
from .show_env.migration_sp_su.sp_to_su_procedure import sp_to_su_procedure
from .show_env.migration_sp_su.su_to_sp_procedure import su_to_sp_procedure
from .show_env.show_user.show_user import DroneUser, ShowUser


def apply_export_procedure(
    show_user: ShowUser,
) -> Tuple[IostarJson, ShowCheckReport]:
    show_check_report = ShowCheckReport(len(show_user.drones_user))
    apply_all_check_from_show_user_procedure(show_user, show_check_report)
    return (
        sp_to_ij_procedure(su_to_sp_procedure(show_user)),
        show_check_report,
    )


def create_show_user(drone_number: int) -> ShowUser:
    """Create a ShowUser object from a JSON file."""
    if not isinstance(drone_number, int):
        msg = f"{drone_number} is not an integer"
        raise TypeError(msg)
    if drone_number < 1:
        msg = f"{drone_number} is not a positive integer"
        raise ValueError(msg)
    return ShowUser(
        drones_user=[
            DroneUser(position_events=[], color_events=[], fire_events=[])
            for _ in range(drone_number)
        ]
    )


def export_show_user_to_iostar_json_string(show_user: ShowUser) -> str:
    """Export a ShowUser object to a IostarJson on the string format."""
    iostar_json, show_check_report = apply_export_procedure(show_user)
    if not (show_check_report.validation):
        show_check_report.get_contenor_report(4, " ")
        msg = "The show is not valid"
        raise ValueError(msg)
    return iostar_json.json()


def export_show_user_to_iostar_json_gcs_string(show_user: ShowUser) -> str:
    """Export a ShowUser object to a JSON file."""
    iostar_json_string = export_show_user_to_iostar_json_string(show_user)
    show_px4 = ij_to_sp_procedure(IostarJson.parse_raw(iostar_json_string))
    iostar_json_gcs = sp_to_ijg_procedure(show_px4)
    return iostar_json_gcs.json()


def global_check_iostar_json_gcs(iostar_json_gcs: IostarJsonGcs) -> bool:
    """Check the validity of an iostar_json_gcs."""
    show_user = sp_to_su_procedure(ijg_to_sp_procedure(iostar_json_gcs))
    show_check_report = ShowCheckReport(len(show_user.drones_user))
    apply_all_check_from_show_user_procedure(show_user, show_check_report)
    return show_check_report.validation
