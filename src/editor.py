from .check.all_check_from_show_user_procedure import (
    apply_all_check_from_show_user_procedure,
)
from .check.show_check_report import ShowCheckReport
from .export_procedure import apply_export_procedure
from .migration.iostar_json.iostar_json_gcs import IostarJsonGCS
from .migration.migration_sp_ij.ij_to_sp_procedure import ij_to_sp_procedure
from .migration.migration_sp_ijg.ijg_to_sp_procedure import ijg_to_sp_procedure
from .migration.migration_sp_ijg.sp_to_ijg_procedure import sp_to_ijg_procedure
from .migration.migration_sp_su.sp_to_su_procedure import sp_to_su_procedure
from .show_user.show_user import DroneUser, ShowUser


# TODO: put a test on this
def create_show_user(drone_number: int) -> ShowUser:
    """Create a ShowUser object from a JSON file."""
    return ShowUser(
        drones_user=[
            DroneUser(position_events=[], color_events=[], fire_events=[])
            for _ in range(drone_number)
        ]
    )


# TODO: put a test on this
def export_show_user_to_iostar_json(show_user: ShowUser) -> str:
    """Export a ShowUser object to a JSON file."""
    iostar_json, show_check_report = apply_export_procedure(show_user)
    if not (show_check_report.validation):
        show_check_report.get_contenor_report(4, " ")
        msg = "The show is not valid"
        raise ValueError(msg)
    return iostar_json.get_json()


# TODO: put a test on this
def export_show_user_to_iostar_json_gcs(show_user: ShowUser) -> str:
    """Export a ShowUser object to a JSON file."""
    iostar_json, show_check_report = apply_export_procedure(show_user)
    show_px4 = ij_to_sp_procedure(iostar_json)
    iostar_json_gcs = sp_to_ijg_procedure(show_px4)
    if not (show_check_report.validation):
        show_check_report.get_contenor_report(4, " ")
        msg = "The show is not valid"
        raise ValueError(msg)
    return iostar_json_gcs.get_json()


# TODO: put a test on this
def global_check_iostar_json(iostar_json_gcs: IostarJsonGCS) -> bool:
    """Check the validity of an iostar_json_gcs."""
    show_user = sp_to_su_procedure(ijg_to_sp_procedure(iostar_json_gcs))
    show_check_report = ShowCheckReport(len(show_user.drones_user))
    apply_all_check_from_show_user_procedure(show_user, show_check_report)
    return show_check_report.validation
