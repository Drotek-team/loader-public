from ..show_px4.show_px4 import ShowPx4
from ..parameter.parameter import Parameter
from .show_simulation_check.simulation_check_procedure import (
    apply_simulation_check_procedure,
)
from .show_px4_check.dance_check_procedure import apply_dance_check_procedure
from .show_check_report import ShowCheckReport
from ..migration.migration_SP_SS.SP_to_SS_procedure import DP_to_SS_procedure
from ..migration.migration_SP_SS.SP_to_DS_procedure import SP_to_SD_procedure
from .show_dev_check.show_dev_check_procedure import (
    apply_show_dev_procedure,
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

    show_dev = SP_to_SD_procedure(show_px4)

    apply_show_dev_procedure(
        show_dev,
        show_check_report.drones_dev_check_report,
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
