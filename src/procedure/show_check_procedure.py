from ..show_px4.show_px4 import ShowPx4
from ..parameter.parameter import Parameter
from .show_simulation_check.simulation_check_procedure import (
    apply_simulation_check_procedure,
)
from .show_px4_check.dance_check_procedure import apply_dance_check_procedure
from .show_check_report import ShowCheckReport
from ..migration.migration_DP_SS.SP_to_SS_procedure import DP_to_SS_procedure
from ..migration.migration_DP_SS.SP_to_DS_procedure import DP_to_DS_procedure
from .drones_simulation_check.drone_simulation_check_procedure import (
    apply_drone_simulation_check_procedure,
)


def apply_show_check_procedure(
    show_px4: ShowPx4,
    show_check_report: ShowCheckReport,
    parameter: Parameter,
) -> None:
    for drone, dance_check_report in zip(
        show_px4, show_check_report.drones_check_report
    ):
        apply_dance_check_procedure(drone, dance_check_report, parameter)

    drones_simulation = DP_to_DS_procedure(show_px4)

    for drone_simulation, drone_simulation_check_report in zip(
        drones_simulation, show_check_report.drones_simulation_check_report
    ):
        apply_drone_simulation_check_procedure(
            drone_simulation,
            drone_simulation_check_report,
            parameter.takeoff_parameter,
            parameter.frame_parameter,
        )

    show_simulation = DP_to_SS_procedure(
        show_px4,
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
