from .....parameter.parameter import IostarParameter, TakeoffParameter
from .....show_simulation.show_simulation import ShowSimulation
from .observed_metrics.observed_metrics import ObservedMetricsSlice
from .performance_check_report import PerformanceCheckReport


def apply_performance_check_procedure(
    show_simulation: ShowSimulation,
    performance_check_report: PerformanceCheckReport,
    iostar_parameter: IostarParameter,
    takeoff_parameter: TakeoffParameter,
) -> None:
    performance_check_report.update_observed_metrics_slices_check_report(
        show_simulation.timecodes
    )
    observed_metrics_slice = ObservedMetricsSlice(
        show_simulation.nb_drones, iostar_parameter, takeoff_parameter
    )
    for simulation_slice, observed_metrics_slice_check_report in zip(
        show_simulation.show_slices,
        performance_check_report.observed_metrics_slices_check_report,
    ):
        observed_metrics_slice.update_observed_metrics(
            simulation_slice.positions,
            simulation_slice.velocities,
            simulation_slice.accelerations,
            observed_metrics_slice_check_report,
            iostar_parameter,
        )
        observed_metrics_slice_check_report.update()
    performance_check_report.update()
