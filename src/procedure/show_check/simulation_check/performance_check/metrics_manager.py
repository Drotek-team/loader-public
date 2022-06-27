from typing import List

from .....parameter.parameter import IostarParameter, TakeoffParameter
from .....show_simulation.show_simulation import ShowSimulationSlice
from .observed_metrics.observed_metrics import ObservedMetrics


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
            observed_metrics.update_observed_metrics(
                position,
                velocity,
                acceleration,
                iostar_parameter,
            )
