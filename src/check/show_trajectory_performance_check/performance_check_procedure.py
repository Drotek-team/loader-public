from ...parameter.parameter import IostarParameter, TakeoffParameter
from ...show_simulation.show_simulation import ShowSimulation
from .observed_metrics.observed_metrics import ObservedMetricsSlice
from .performance_check_report import PerformanceCheckReport


def apply_performance_check_procedure(
    show_simulation: ShowSimulation,
    performance_check_report: PerformanceCheckReport,
    iostar_parameter: IostarParameter,
    takeoff_parameter: TakeoffParameter,
) -> None:
    observed_metrics_slice = ObservedMetricsSlice(
        show_simulation.nb_drones, iostar_parameter, takeoff_parameter
    )
    for simulation_slice, performance_slice_check_report in zip(
        show_simulation.show_slices,
        performance_check_report.performance_slices_check_report,
    ):
        observed_metrics_slice.update_observed_metrics(
            simulation_slice.in_dance_drone_indices,
            simulation_slice.positions,
            simulation_slice.velocities,
            simulation_slice.accelerations,
            performance_slice_check_report,
            iostar_parameter,
        )
        performance_slice_check_report.update()
    performance_check_report.update()
