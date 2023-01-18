from ...report import Contenor
from ...show_env.migration_sp_su.su_to_sp_procedure import su_to_sp_procedure
from ...show_env.show_user.show_user import ShowUser
from .dance_size_check.dances_size_check_procedure import (
    apply_dance_size_check_procedure,
)
from .events_format_check.events_format_check_procedure import (
    apply_events_format_check_procedure,
)


# TODO: I mean wtf there is not test for this ???
def apply_show_px4_check_procedure(show_user: ShowUser) -> Contenor:
    show_px4_check_contenor = Contenor("show px4 check procedure")
    show_px4 = su_to_sp_procedure(
        show_user,
    )
    for drone_px4 in show_px4:
        show_px4_check_contenor.add_error_message(
            apply_events_format_check_procedure(
                drone_px4,
            )
        )
        show_px4_check_contenor.add_error_message(
            apply_dance_size_check_procedure(
                drone_px4,
            )
        )
    return show_px4_check_contenor
