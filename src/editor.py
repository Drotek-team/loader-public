from typing import Tuple

from pydantic import NonNegativeInt

from .check.all_check_from_show_user import apply_all_check_from_show_user
from .report import Contenor
from .show_env.iostar_json.iostar_json import IostarJson
from .show_env.iostar_json.iostar_json_gcs import IostarJsonGcs
from .show_env.migration_sp_ij.sp_to_ij import su_to_ij
from .show_env.migration_sp_ijg.ijg_to_su import ijg_to_su
from .show_env.migration_sp_ijg.su_to_ijg import su_to_ijg
from .show_env.show_user.show_user import DroneUser, ShowUser


def create_empty_show_user(drone_number: NonNegativeInt) -> ShowUser:
    """Create an empy ShowUser object with 'drone_number' drone."""
    return ShowUser(
        drones_user=[
            DroneUser(position_events=[], color_events=[], fire_events=[])
            for _ in range(drone_number)
        ]
    )


# TODO: test this
def import_show_user_from_iostar_json_string(iostar_json_string: str) -> ShowUser:
    """Import a ShowUser object from a iostar_json JSON file."""
    iostar_json_gcs = IostarJsonGcs.parse_raw(iostar_json_string)
    return ijg_to_su(iostar_json_gcs)


# TODO: make specific check (performane,collision)


def apply_export_to_iostar_json(
    show_user: ShowUser,
) -> Tuple[IostarJson, Contenor]:
    """Convert a show user into an iostar json and check it."""
    check_contenor = apply_all_check_from_show_user(show_user)
    return (su_to_ij(show_user), check_contenor)


def apply_export_to_iostar_json_gcs(
    show_user: ShowUser,
) -> Tuple[IostarJsonGcs, Contenor]:
    """Convert a show user into an iostar json gcs and check it."""
    check_contenor = apply_all_check_from_show_user(show_user)
    return (su_to_ijg(show_user), check_contenor)


def export_show_user_to_iostar_json_string(show_user: ShowUser) -> str:
    """Export a ShowUser object to a IostarJson on the string format."""
    iostar_json, show_check_report = apply_export_to_iostar_json(show_user)
    if not (show_check_report.user_validation):
        show_check_report.display_message()
        msg = "The show is not valid"
        raise ValueError(msg)
    return iostar_json.json()


def export_show_user_to_iostar_json_gcs_string(show_user: ShowUser) -> str:
    """Export a ShowUser object to a iostar_json_gcs JSON file."""
    iostar_json_gcs, show_check_report = apply_export_to_iostar_json_gcs(show_user)
    if not (show_check_report.user_validation):
        show_check_report.display_message()
        msg = "The show is not valid"
        raise ValueError(msg)
    return iostar_json_gcs.json()


# TODO: the ConfigurationGcs is not check here, need to add something
def global_check_iostar_json_gcs(iostar_json_gcs: IostarJsonGcs) -> bool:
    """Check the validity of an iostar_json_gcs."""
    show_user = ijg_to_su(iostar_json_gcs)
    show_check_report = apply_all_check_from_show_user(show_user)
    return show_check_report.user_validation
