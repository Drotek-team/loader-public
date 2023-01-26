from ...report import Contenor
from ...show_env.migration_sp_su.su_to_sp import su_to_sp
from ...show_env.show_user.show_user import ShowUser
from .dance_size_check.dances_size_check import apply_dance_size_check
from .events_format_check.events_format_check import apply_events_format_check


def apply_show_px4_check(show_user: ShowUser) -> Contenor:
    show_px4_check_contenor = Contenor("show px4 check")
    show_px4 = su_to_sp(
        show_user,
    )
    for drone_px4 in show_px4:
        show_px4_check_contenor.add_error_message(
            apply_events_format_check(
                drone_px4,
            )
        )
        show_px4_check_contenor.add_error_message(
            apply_dance_size_check(
                drone_px4,
            )
        )
    return show_px4_check_contenor
