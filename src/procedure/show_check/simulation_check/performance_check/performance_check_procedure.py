from .....parameter.parameter import IostarParameter
from .....show_simulation.show_simulation import ShowSimulation
from .metrics_manager import MetricsManager
from .performance_check_report import PerformanceCheckReport


def apply_performance_check_procedure(
    show_simulation: ShowSimulation,
    performance_check_report: PerformanceCheckReport,
    iostar_parameter: IostarParameter,
) -> None:
    metrics_manager = MetricsManager(show_simulation.nb_drones)
    for simulation_slice in show_simulation.slices:
        metrics_manager.update_observed_metric_values(
            simulation_slice, iostar_parameter
        )
        performance_check_report.update_drones_performance_check_report(
            simulation_slice.timecode, metrics_manager.get_observed_metric_report()
        )
    performance_check_report.update()
