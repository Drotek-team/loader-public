from ..migration.migration_SD_ST.SD_to_STC_procedure import SD_to_STC_procedure
from ..migration.migration_SD_ST.SD_to_STP_procedure import SD_to_STP_procedure
from ..migration.migration_SP_SD.SP_to_SD_procedure import SP_to_SD_procedure
from ..migration.migration_STC_SSC.STC_to_SSC_procedure import STC_to_SS_procedure
from ..parameter.parameter import Parameter
from ..show_px4.show_px4 import ShowPx4
from .show_check_report import (
    ShowCheckReport,
    ShowDevCheckReport,
    ShowPx4CheckReport,
    ShowSimulationCollisionCheckReport,
    ShowTrajectoryPerformanceCheckReport,
)
from .show_dev_check.show_dev_check_procedure import apply_show_dev_procedure
from .show_px4_check.show_px4_chek_procedure import apply_show_px4_check_procedure
from .show_simulation_collision_check.show_simulation_collision_check_procedure import (
    apply_show_simulation_collision_check_procedure,
)
from .show_trajectory_performance_check.show_trajectory_performance_check_procedure import (
    apply_show_trajectory_performance_check_procedure,
)


def apply_all_check_from_show_px4_procedure(
    show_px4: ShowPx4,
    parameter: Parameter,
) -> ShowCheckReport:

    # PX4 part
    show_px4_check_report = ShowPx4CheckReport(show_px4.nb_drone)
    apply_show_px4_check_procedure(show_px4, show_px4_check_report, parameter)

    # Dev Part
    show_dev = SP_to_SD_procedure(show_px4)
    show_dev_check_report = ShowDevCheckReport(show_dev.nb_drones)
    apply_show_dev_procedure(
        show_dev,
        show_dev_check_report,
        parameter.takeoff_parameter,
        parameter.frame_parameter,
    )

    # Performance part
    show_trajectory_performance = SD_to_STP_procedure(
        show_dev, parameter.frame_parameter
    )
    show_trajectory_performance_check_report = ShowTrajectoryPerformanceCheckReport(
        show_trajectory_performance.nb_drones
    )
    apply_show_trajectory_performance_check_procedure(
        show_trajectory_performance,
        show_trajectory_performance_check_report,
    )

    # Collision part
    show_trajectory_collision = SD_to_STC_procedure(
        show_dev,
        parameter.frame_parameter,
        parameter.takeoff_parameter,
        parameter.land_parameter,
    )
    show_simulation = STC_to_SS_procedure(
        show_trajectory_collision,
    )
    show_simulation_collision_check_report = ShowSimulationCollisionCheckReport(
        show_simulation.frames
    )
    apply_show_simulation_collision_check_procedure(
        show_simulation,
        show_simulation_collision_check_report,
        parameter.iostar_parameter,
    )
    show_check_report = ShowCheckReport(
        show_px4_check_report,
        show_dev_check_report,
        show_trajectory_performance_check_report,
        show_simulation_collision_check_report,
    )

    show_check_report.update()
    return show_check_report
