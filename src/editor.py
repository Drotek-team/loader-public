from .migration.migration_sp_ij.ij_to_sp_procedure import ij_to_sp_procedure
from .migration.migration_sp_ijg.sp_to_ijg_procedure import sp_to_ijg_procedure
from .procedure.export_procedure import apply_export_procedure
from .show_user.show_user import DroneUser, ShowUser


def create_show_user(drone_number: int) -> ShowUser:
    """Create a ShowUser object from a JSON file."""
    return ShowUser(
        drones_user=[
            DroneUser(position_events=[], color_events=[], fire_events=[])
            for _ in range(drone_number)
        ]
    )


def export_show_user_to_iostar_json(show_user: ShowUser) -> str:
    """Export a ShowUser object to a JSON file."""
    iostar_json, show_check_report = apply_export_procedure(show_user)
    if not (show_check_report.validation):
        show_check_report.get_contenor_report(4, " ")
        msg = "The show is not valid"
        raise ValueError(msg)
    return iostar_json.get_json()


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
