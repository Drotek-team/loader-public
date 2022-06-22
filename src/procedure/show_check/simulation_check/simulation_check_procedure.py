from ....show_simulation.show_simulation import ShowSimulation
from .collision_check.collision_check_procedure import apply_collision_check_procedure
from .performance_check.performance_check_procedure import (
    apply_performance_check_procedure,
)
from .simulation_check_report import SimulationCheckReport


def apply_simulation_check_procedure(
    show_simulation: ShowSimulation,
    simulation_check_report: SimulationCheckReport,
) -> None:
    apply_performance_check_procedure(
        show_simulation, simulation_check_report.performance_check_report
    )
    apply_collision_check_procedure(
        show_simulation, simulation_check_report.collision_check_report
    )
