from .performance_check.performance_check_report import (
    PerformanceCheckReport,
)
from ...parameter.parameter import IostarParameter, TakeoffParameter
from ...show_simulation.show_simulation import ShowSimulation
from .collision_check.collision_check_procedure import apply_collision_check_procedure
from .performance_check.performance_check_procedure import (
    apply_performance_check_procedure,
)
from .simulation_check_report import SimulationCheckReport, CollisionCheckReport


def apply_simulation_check_procedure(
    show_simulation: ShowSimulation,
    simulation_check_report: SimulationCheckReport,
    iostar_parameter: IostarParameter,
    takeoff_parameter: TakeoffParameter,
) -> None:
    simulation_check_report.performance_check_report = PerformanceCheckReport(
        show_simulation.frames
    )
    apply_performance_check_procedure(
        show_simulation,
        simulation_check_report.performance_check_report,
        iostar_parameter,
        takeoff_parameter,
    )
    simulation_check_report.collision_check_report = CollisionCheckReport(
        show_simulation.frames
    )
    apply_collision_check_procedure(
        show_simulation,
        simulation_check_report.collision_check_report,
        iostar_parameter,
    )
    simulation_check_report.update()
