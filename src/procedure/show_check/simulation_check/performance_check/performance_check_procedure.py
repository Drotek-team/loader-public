from .....parameter.parameter import IostarParameter
from .....show_simulation.show_simulation import ShowSimulation
from .observed_metrics.observed_metrics import ObservedMetricsSlice
from .performance_check_report import PerformanceCheckReport


def apply_performance_check_procedure(
    show_simulation: ShowSimulation,
    performance_check_report: PerformanceCheckReport,
    iostar_parameter: IostarParameter,
) -> None:
    observed_metrics_slice = ObservedMetricsSlice()
    for simulation_slice, observed_metrics_slice_check_report in zip(
        show_simulation.slices,
        performance_check_report.observed_metrics_slices_check_report,
    ):
        observed_metrics_slice.update_observed_metrics(
            simulation_slice.positions,
            simulation_slice.velocities,
            simulation_slice.accelerations,
            observed_metrics_slice_check_report,
            iostar_parameter,
        )
    performance_check_report.update()
