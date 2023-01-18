from ..report import Contenor
from ..show_env.show_user.show_user import ShowUser
from .collision_check.show_simulation_collision_check_procedure import (
    apply_show_simulation_collision_check_procedure,
)
from .performance_check.show_trajectory_performance_check_procedure import (
    apply_show_trajectory_performance_check_procedure,
)
from .show_px4_check.show_px4_check_procedure import apply_show_px4_check_procedure
from .show_user_check.show_user_check_procedure import apply_show_user_check_procedure


def apply_all_check_from_show_user_procedure(
    show_user: ShowUser,
) -> Contenor:
    check_contenor = Contenor("Check")
    check_contenor.add_error_message(apply_show_user_check_procedure(show_user))
    if not (check_contenor["show user check procedure"].user_validation):
        return check_contenor
    check_contenor.add_error_message(apply_show_px4_check_procedure(show_user))
    if not (check_contenor["show px4 check procedure"].user_validation):
        return check_contenor
    apply_show_trajectory_performance_check_procedure(
        show_user,
    )
    apply_show_simulation_collision_check_procedure(
        show_user,
    )
    return check_contenor
