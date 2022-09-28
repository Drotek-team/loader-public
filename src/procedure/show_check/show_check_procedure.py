from ...drones_user.drones_user import DronesUser
from ...family_manager.family_manager import FamilyUser
from ...parameter.parameter import Parameter
from ...show_simulation.show_simulation import ShowSimulation, get_slices
from ..show_check.simulation_check.simulation_check_procedure import (
    apply_simulation_check_procedure,
)
from .drone_check.dance_check_procedure import apply_dance_check_procedure
from .family_manager_check.family_manager_check_procedure import (
    apply_family_check_procedure,
)
from .show_check_report import ShowCheckReport


def apply_show_check_procedure(
    drones_user: DronesUser,
    family_manager: FamilyUser,
    show_check_report: ShowCheckReport,
    parameter: Parameter,
) -> None:
    for drone, dance_check_report in zip(
        drones_user.drones, show_check_report.drones_check_report
    ):
        apply_dance_check_procedure(drone, dance_check_report, parameter)
    apply_family_check_procedure(
        drones_user,
        family_manager,
        parameter.frame_parameter,
        parameter.json_convertion_constant,
        parameter.family_parameter,
        show_check_report.family_check_report,
    )
    show_simulation = ShowSimulation(
        get_slices(
            drones_user.get_trajectory_simulation_manager(
                parameter.json_convertion_constant
            ),
            parameter.frame_parameter,
            parameter.takeoff_parameter,
            parameter.land_parameter,
        )
    )
    apply_simulation_check_procedure(
        show_simulation,
        show_check_report.simulation_check_report,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
    )
    show_check_report.update()
