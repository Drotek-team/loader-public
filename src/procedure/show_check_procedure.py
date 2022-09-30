from ..drones_px4.drones_px4 import DronesPx4
from ..show_user.show_user import FamilyUser
from ..parameter.parameter import Parameter
from .show_simulation_check.simulation_check_procedure import (
    apply_simulation_check_procedure,
)
from .drones_px4_check.dance_check_procedure import apply_dance_check_procedure
from .family_user_check.family_user_check_procedure import (
    apply_family_check_procedure,
)
from .show_check_report import ShowCheckReport
from .migration_DP_SS.DP_to_SS_procedure import DP_to_SS_procedure


def apply_show_check_procedure(
    drones_px4: DronesPx4,
    family_user: FamilyUser,
    show_check_report: ShowCheckReport,
    parameter: Parameter,
) -> None:
    for drone, dance_check_report in zip(
        drones_px4.drones, show_check_report.drones_check_report
    ):
        apply_dance_check_procedure(drone, dance_check_report, parameter)
    apply_family_check_procedure(
        drones_px4,
        family_user,
        parameter.frame_parameter,
        parameter.family_parameter,
        show_check_report.family_check_report,
    )
    show_simulation = DP_to_SS_procedure(
        drones_px4,
        parameter.frame_parameter,
        parameter.takeoff_parameter,
        parameter.land_parameter,
    )

    apply_simulation_check_procedure(
        show_simulation,
        show_check_report.simulation_check_report,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
    )
    show_check_report.update()
