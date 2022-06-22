from .....parameter.parameter import IostarParameter, TakeoffParameter
from .....show_simulation.show_simulation import ShowSimulationSlice
from .check_metrics.check_metrics import ObservedMetrics


class MetricsManager:
    def __init__(
        self,
        nb_drones: int,
        iostar_parameter: IostarParameter,
        takeoff_parameter: TakeoffParameter,
    ):
        self.slice_observed_metrics = [
            ObservedMetrics(iostar_parameter, takeoff_parameter)
            for _ in range(nb_drones)
        ]

    def update_observed_metric_values(
        self,
        show_simulation_slice: ShowSimulationSlice,
        iostar_parameter: IostarParameter,
    ) -> None:

        for observed_metrics, position, velocity, acceleration in zip(
            self.slice_observed_metrics,
            show_simulation_slice.positions,
            show_simulation_slice.velocities,
            show_simulation_slice.accelerations,
        ):
            observed_metrics.update_metrics(
                position,
                velocity,
                acceleration,
                iostar_parameter,
            )

    def check_observed_metric_report(
        self,
        slice_observed_metrics_report,
    ) -> None:
        for observed_metrics, observed_metrics_report in zip(
            self.slice_observed_metrics, slice_observed_metrics_report
        ):
            for metric, metric_report in zip(
                observed_metrics.get_metrics(),
                observed_metrics_report.get_metrics_report(),
            ):
                metric_report.update(metric.validation_ratio >= 1.0)
