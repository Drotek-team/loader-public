from .....parameter.parameter import TimecodeParameter
from .....show_simulation.show_simulation import ShowSimulation
from ..frame_constraint import FrameConstraint
from .metrics_manager import MetricsManager
from .performance_check_report import PerformanceCheckReport


def apply_performance_check_procedure(
    show_simulation: ShowSimulation,
    timecode_parameter: TimecodeParameter,
    performance_check_report: PerformanceCheckReport,
) -> None:
    metrics_manager = MetricsManager(len(show_simulation.nb_drones))
    for simulation_slice in show_simulation.slices:
        metrics_manager.update_observed_metric_values(simulation_slice)
        metrics_manager.update_observed_metric_report(frame, performance_check_report)
