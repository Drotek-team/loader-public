from src.procedure.export_procedure import apply_export_procedure
from src.show_user.show_user import DroneUser, ShowUser


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
