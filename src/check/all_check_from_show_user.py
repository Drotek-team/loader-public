from ..report.report import Contenor
from ..show_env.show_user.show_user import ShowUser
from .collision_check.show_simulation_collision_check import (
    apply_show_simulation_collision_check,
)
from .performance_check.show_trajectory_performance_check import (
    apply_show_trajectory_performance_check,
)
from .show_px4_check.show_px4_check import apply_show_px4_check
from .show_user_check.show_user_check import apply_show_user_check


def apply_all_check_from_show_user(
    show_user: ShowUser,
) -> Contenor:
    check_contenor = Contenor("Check")
    check_contenor.add_error_message(apply_show_user_check(show_user))
    if not (check_contenor["show user check"].user_validation):
        return check_contenor
    check_contenor.add_error_message(apply_show_px4_check(show_user))
    if not (check_contenor["show px4 check"].user_validation):
        return check_contenor
    check_contenor.add_error_message(
        apply_show_trajectory_performance_check(
            show_user,
        )
    )
    check_contenor.add_error_message(
        apply_show_simulation_collision_check(
            show_user,
        )
    )
    return check_contenor
